Ở đây ta sẽ thấy điều kiện để có flag là gọi được hàm win. Nếu chơi thắng chương trình được 10 lần thì sẽ gọi hàm win.
Nhìn vào hàm Play sẽ thấy khi pass qua được đoạn strstr(choice, pokemonss[computer]) thì Play sẽ return 1.
Thực ra có 2 cách pass qua đoạn này. Cách 1 là các bạn bruteforce =)) với tỉ lệ xấp xỉ 0,001%. Còn cách thứ 2 thì các bạn để ý chỗ hàm strstr(a,b), nó sẽ trả về con trỏ trỏ đến vị trí đầu tiên chuỗi b xuất hiện trong chuỗi a. Nên chỉ cần chuỗi b có tồn tại trong a là được, các bạn chỉ cần nhập "BulbasaurCharmanderSquirtle" 10 lần là có thể lấy được flag :Đ.

