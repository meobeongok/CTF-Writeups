// g++ -std=c++17 -Wshadow -z relro -z now -no-pie -Wall -s -o game game.cpp -DLOCAL

#include <bits/stdc++.h>
#include <unistd.h>

using namespace std;

#define N 20
#define M 200

// /* Compile with -DLOCAL flag */
// void debug_out() { cerr << endl; }
 
// template <typename Head, typename... Tail>
// void debug_out(Head H, Tail... T) {
//   cerr << " " << to_string(H);
//   debug_out(T...);
// }
 
// #ifdef LOCAL
// #define debug(...) cerr << "[" << #__VA_ARGS__ << "]:", debug_out(__VA_ARGS__)
// #else
// #define debug(...) 42
// #endif

class user {
    private:
        string username;
        string detail;
        int admin;
        int score;
    public:
        user() {
            username = "Unknown player";
            detail = "Im not Cobra";
            admin = 0;
            score = 0;
        }

        user operator=(const user &u) {
            username = u.username;
            detail = u.detail;
            admin = u.admin;
            score = u.score;
        }

        void update(char* name, int s) {
            if (score < s) {                  
                username = string(name);     
                score = s;
            }
        }

        void info() {
            cout << "Username: " << username << '\n';
            cout << "Detail: " << detail << '\n';
            cout << "Admin: " << admin << '\n';
            cout << "Score: " << score << '\n';
            cout << '\n';
        }

        ~user() {
            if (admin && detail == "My name is Cobra" && score == 2000) {
                system("/bin/sh");
            }
        }
};

char gold_map[N][N];
char name[M];
user top;

map<char, int> mp({{'A', 0}, {'W', 1}, {'S', 2}, {'D', 3}});
char d1[] = { 0, -1, 1, 0 };
char d2[] = { -1, 0, 0, 1 };

void get_name() {
    cout << "Input your username: ";
    char tmp[M] = { '\x00' };
    cin.getline(tmp, M - 1);
    memcpy(name, tmp, M);
}

bool valid(int x, int y) {
    return (~x && ~y && x < N && y < N && gold_map[x][y] != '#');
}

/* Check if you can reach at least 5 star 
in random map, just ignore it :)))) */
bool check_validmap() { 
    if (gold_map[0][0] == 'x') {
        bool test[N][N] = { false };
        int cnt = 0;
        vector<pair<int, int>> q;
        q.push_back({ 0, 0 });
        test[0][0] = true;
        for (int i = 0; i < (int)q.size(); i++) {
            // debug(q[i].first, q[i].second);
            for (int j = 0; j < 4; j++) {
                int new_row = q[i].first + d1[j];   
                int new_col =  q[i].second + d2[j];
                if (valid(new_row, new_col) && !test[new_row][new_col]) {
                    test[new_row][new_col] = true;
                    q.push_back({ new_row, new_col });
                    if (gold_map[new_row][new_col] == '*') {
                        cnt++;
                    }
                    // debug(new_row, new_col);
                }
            }
        }        
        if (cnt >= 5) {
            return true;
        }
    }
    return false;
}

void init() {
    while (true) {
        srand(time(NULL));
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (i == 0 && j == 0) {
                    gold_map[i][j] = 'x';
                } else {
                    int z = rand() % 5;
                    if (z == 0) {
                        gold_map[i][j] = '*';
                    } else if (z == 1) {
                        gold_map[i][j] = '#';
                    } else {
                        gold_map[i][j] = '.';
                    }                
                }
            }
        }
        if (check_validmap()) {            
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    cout << gold_map[i][j] << ' ';
                }
                cout << '\n';
            }
            break;
        }
    }
}

void update(int score) {
    user old;
    old = top;
    top.update(name, score);
    cout << '\n' << "Previous top player:" << '\n';
    old.info();
    cout << '\n' <<  "New top player:" << '\n';
    top.info();
}

void play_game() {
    cout << "It is on beta version, sorry if sometime you cannot play T^T" << '\n';
    init();
    int row = 0, col = 0, count = 0, new_row = 0, new_col = 0;
    cout << "You are now at (0, 0)" << '\n';
    cout << "Enter ASDW to move, max 1000 step, * are gold, # are trap and you will die ^^" << '\n';
    cout << "Collect 5 star in minimun of move" << '\n';
    cout << "Input move: ";
    string tmp;
    cin >> tmp;
    tmp = tmp.substr(0, 1000);
    cout << "Your move: " << tmp << '\n';
    for (auto c : tmp) {
        c = toupper(c);
        if (mp.count(c)) {
            new_row = row + d1[mp[c]];
            new_col = col + d2[mp[c]];         
        } else {
            cout << "Invalid character !" << '\n';
            break;
        }
        if (valid(new_row, new_col)) {
            row = new_row;
            col = new_col;
            if (gold_map[row][col] == '*') {
                gold_map[row][col] = '.';
                count++;
            }
        } else {
            cout << "Invalid move !" << '\n';
            // debug(row, col, new_row, new_col);
            break;
        }
    }
    cout << "You getting " << count << " start !" << '\n';
    if (count >= 5) {
        int score = 1000 - tmp.size();
        cout << "Your score: " << score << '\n';
        getchar();
        get_name();
        update(score);
    } else {
        cout << "Not enough start !" << '\n';
    }
}

int main() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    cout << "Welcome to Cobra trash game :)))" << '\n';
    
    int run = 1;
    while (run) {
        cout << "1. Play game" << '\n';
        cout << "2. Exit" << '\n';
        int choice = 0;
        cin >> choice; 
        switch (choice) {
            case 1:
                play_game();
                break;          
            case 2:
                run = 0;
                break;            
            default:
                cout << "Not valid choice!!!" << '\n';
                break;
        }
    }
    cout << "Bye" << '\n';

    return 0;
}
