import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime

def process_whatsapp_chat(file_path):
    try:
        # read chat file
        with open(file_path, 'r', encoding='utf-8') as file:
            chat_lines = file.readlines()
        
        messages = []
        pattern = r'\[(\d{2}/\d{2}/\d{2}), (\d{2}\.\d{2}\.\d{2})\] ([^:]+): (.+)'
        
        print("Membaca file chat...")
        print(f"Total baris yang dibaca: {len(chat_lines)}")
        
        for line in chat_lines:
            # Clean character unicode(Sticker)
            clean_line = line.replace('[U+200E]', '').strip()
            match = re.match(pattern, clean_line)
            
            if match:
                date, time, user, message = match.groups()
                # Filter chat system
                if not any(keyword in message for keyword in 
                         ['was added', 'sticker omitted', 'Messages and calls are end-to-end encrypted']):
                    messages.append({
                        'date': date,
                        'time': time,
                        'user': user.strip(),
                        'message': message.strip()
                    })
        
        print(f"Total pesan yang berhasil diproses: {len(messages)}")
        # Debug: Show some first chat
        if messages:
            print("\nContoh beberapa pesan pertama:")
            for msg in messages[:3]:
                print(msg)
        else:
            print("\nTidak ada pesan yang berhasil diproses. Beberapa baris pertama dari file:")
            for line in chat_lines[:5]:
                print(f"Baris mentah: {line.strip()}")
        
        return pd.DataFrame(messages) if messages else None
    
    except Exception as e:
        print(f"Error detail: {str(e)}")
        return None

def analyze_chat(df):
    if df is None or df.empty:
        print("Error: Tidak ada data untuk dianalisis")
        return
    
    try:
        # Count user chats
        message_counts = df['user'].value_counts()
        
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