<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin" style="border: 5;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>

<h1 align="center"><b></b></h1>


# Giới thiệu
* **Tên môn học:** Truy xuất thông tin - CS419.P21
* **Năm học:** HK2 (2024 - 2025)
* **Giảng viên**: Nguyễn Trọng Chỉnh
* **Sinh viên thực hiện:**
  
  | STT | MSSV     | Họ và Tên        | Email                   |
  |-----|----------|------------------|-------------------------|
  |1    | 22520083 | Trịnh Thị Lan Anh  | 22520083@gm.uit.edu.vn |
  |2    | 22520363 | Lê Văn Giáp | 22520363@gm.uit.edu.vn |
  |3    | 22520375 | Vương Dương Thái Hà | 22520375@gm.uit.edu.vn |


# Channel 14 Retrieval Model
Kênh 14 (kenh14.vn) là một trong những trang báo điện tử giải trí – xã hội hàng đầu tại Việt Nam, sở hữu lượng truy cập lớn và đặc biệt thu hút giới trẻ nhờ nội dung đa dạng, phong phú từ tin tức đời sống, xã hội, giải trí đến giáo dục. Nhằm tận dụng nguồn dữ liệu khổng lồ và liên tục cập nhật này, chúng tôi đã xây dựng một hệ thống truy vấn thông minh, tự động thu thập (crawl), xử lý và trích xuất thông tin từ trang web kenh14.vn.

Hệ thống được thiết kế để nhận câu truy vấn từ người dùng và trả về danh sách các bài báo liên quan nhất, dựa trên các mô hình truy xuất thông tin hiện đại như Vector Space Model (VSM) và BM25. Quá trình này bao gồm các bước: tự động thu thập dữ liệu bài viết, chuẩn hóa và xây dựng chỉ mục ngược, sau đó áp dụng thuật toán đánh giá mức độ liên quan giữa truy vấn và tài liệu. Nhờ đó, hệ thống không chỉ giúp người dùng nhanh chóng tiếp cận các thông tin cần thiết mà còn góp phần nâng cao trải nghiệm tìm kiếm trên nền tảng dữ liệu lớn, đa dạng của Kênh 14.



## Công nghệ sử dụng
[![Node JS](https://img.shields.io/badge/node.js-339933?style=for-the-badge&logo=Node.js&logoColor=white)](https://nodejs.org/en)
[![MongoDB](https://img.shields.io/badge/-MongoDB-13aa52?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/docker-257bd6?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Nltk](https://img.shields.io/badge/NLTK-3.7-blue)

### Frontend:
- **HTML, CSS, JS**: Để xây dựng giao diện người dùng.
- **Material-UI**: Thư viện giao diện người dùng để tạo các thành phần UI đẹp mắt.

### Backend:
- **Fast API**: Framework để xây dựng API 
- **MongoDB**: Cơ sở dữ liệu NoSQL để lưu trữ dữ liệu người dùng và cuộc trò chuyện.
- **Mongoose**: Thư viện ORM để tương tác với MongoDB.

### Docker:
- Docker được sử dụng để container hóa ứng dụng, bao gồm cả frontend, backend và MongoDB.

---

## Cách chạy code

### Bước 1: Clone dự án
```bash
git clone <repository-url>
cd <repository-folder>
```
### Bước 2: Cấu hình môi trường

- **Tạo file .env trong thư mục backend và thêm các biến môi trường:
```bash
git clone <repository-url>
cd <repository-folder>
```
### Bước 3: Chạy ứng dụng với Docker
```
docker-compose up --build

```

