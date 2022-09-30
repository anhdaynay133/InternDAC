*** Nội dung Phase1: 
1. Crawl data từ trang tuoitre.vn bằng thư viện BeautifulSoup4
2. Create database bằng Sql Alchemy ORM trong python 
3. Import data vào trong database bằng SQL Alchelmy 
4. Thiết lập crontab chạy crawl hằng ngày trên Ubuntu

Các bước đặt lịch Crawl data hằng ngày trên ubuntu :

- Vào terminal trên ubuntu và trỏ tới đường dẫn cd /mnt/d/Python_Code/A1_TRAINING_NongVanToan/Phase1

- Sau đó sẽ truyền đường dẫn export PYTHONPATH=${pwd}

- Câu lệnh thực hiện crontab -e: */90 * * * * python3 /mnt/d/Python_Code/A1_TRAINING_NongVanToan/Phase1/daily_crawl.py > /mnt/d/Python_Code/A1_TRAINING_NongVanToan/Phase1/check_crawl.log 2>&1

- Tiếp theo sẽ tiến hành chạy lệnh service cron start để tiến hành crawl sau mỗi 90p.

- File check_crawl.log sẽ trả về thông tin kết quả sau khi crawl xong


*** Nội dung  Phase2:
Tạo input cho recommendation cụ thể nếu có một bài báo thì có thể gợi ý cho người đọc các bài báo liên quan nhất đã được crawl
Yêu cầu: Sử dụng luigi để xây dựng data pipeline.
Pipeline: read raw -> đưa qua model -> có kết quả bài báo chuyên mục gì, lưu ra db mới.
Output: Đưa vào 1 bài báo, kết quả cho ra 1 bài báo tương tự trong cùng category mình lấy được.
Nội dung pipeline:
1. Đọc file input đầu vào
2. Crawl data từ url file input
3. Lưu data crawl vào file json 
4. Import data vào database
5. Xuất ra 5 bài báo liên quan cùng category 