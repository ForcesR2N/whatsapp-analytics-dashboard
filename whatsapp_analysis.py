import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime

def is_phone_number(username: str) -> bool:
    """
    Checks if a username contains an Indonesian phone number pattern.
    This function looks for patterns like '+62' followed by digits,
    which is common in Indonesian phone numbers.
    """
    # Pattern to match Indonesian phone numbers
    phone_pattern = r'\+62\s*\d'
    return bool(re.search(phone_pattern, username))

def process_whatsapp_chat(file_path):
    try:
        # read chat file
        with open(file_path, 'r', encoding='utf-8') as file:
            chat_lines = file.readlines()
        
        messages = []
        # Updated pattern to handle WhatsApp date/time format
        pattern = r'\[(\d{2}/\d{1,2}/\d{2}), (\d{2}\.\d{2}\.\d{2})\] ([^:]+): (.+)'
        
        print("Membaca file chat...")
        print(f"Total baris yang dibaca: {len(chat_lines)}")
        
        filtered_numbers = set()  # To keep track of filtered phone numbers
        
        for line in chat_lines:
            # Clean character unicode
            clean_line = line.replace('[U+200E]', '').strip()
            match = re.match(pattern, clean_line)
            
            if match:
                date, time, user, message = match.groups()
                user = user.strip()
                message = message.strip()
                
                # Check if the user appears to be a phone number
                if is_phone_number(user):
                    filtered_numbers.add(user)
                    continue
                
                # Only add non-system messages and non-empty messages
                if user and message and not any(keyword in message for keyword in 
                         ['was added', 'sticker omitted', 'Messages and calls are end-to-end encrypted']):
                    messages.append({
                        'date': date,
                        'time': time,
                        'user': user,
                        'message': message
                    })
        
        # Print debugging information
        print(f"\nTotal pesan yang berhasil diproses: {len(messages)}")
        if filtered_numbers:
            print("\nNomor telepon yang difilter:")
            for num in filtered_numbers:
                print(f"- {num}")
        
        # Create DataFrame and clean data
        df = pd.DataFrame(messages) if messages else None
        if df is not None:
            # Remove any remaining rows with empty users or messages
            df = df.dropna(subset=['user', 'message'])
            # Remove rows where user is just whitespace
            df = df[df['user'].str.strip().astype(bool)]
            
        return df
    
    except Exception as e:
        print(f"Error detail: {str(e)}")
        return None

def analyze_chat(df):
    if df is None or df.empty:
        print("Error: Tidak ada data untuk dianalisis")
        return
    
    try:
        # Count user chats and filter out users with zero messages
        message_counts = df['user'].value_counts()
        message_counts = message_counts[message_counts > 0]
        
        if message_counts.empty:
            print("Tidak ada data pesan yang valid untuk divisualisasikan")
            return
            
        # Create visualization
        plt.figure(figsize=(12, 6))
        sns.barplot(x=message_counts.values, y=message_counts.index)
        plt.title('Jumlah Pesan per Anggota Grup WhatsApp')
        plt.xlabel('Jumlah Pesan')
        plt.ylabel('Nama Anggota')
        plt.tight_layout()
        
        # save grafik
        plt.savefig('chat_analysis.png')
        plt.show()
        
        # Print statistik
        print("\n=== Statistik Chat ===")
        print(f"Total pesan dalam grup: {len(df)}")
        print(f"Jumlah anggota aktif: {len(message_counts)}")
        print("\nTop 5 pengirim pesan terbanyak:")
        for user, count in message_counts.head().items():
            print(f"{user}: {count} pesan")
            
    except Exception as e:
        print(f"Error saat menganalisis data: {str(e)}")

def main():
    file_path = r'D:\Mapel\Machine Learning\Whatsapp Analysis\WA_Chat.txt'
    
    print("=== Program Analisis Chat WhatsApp ===")
    print("Memulai analisis...")
    
    df = process_whatsapp_chat(file_path)
    
    if df is not None and not df.empty:
        analyze_chat(df)
        print("\nAnalisis selesai! Grafik telah disimpan sebagai 'chat_analysis.png'")
    else:
        print("Program berhenti karena terjadi error.")

if __name__ == "__main__":
    main()