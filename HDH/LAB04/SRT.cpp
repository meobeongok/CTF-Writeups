#include <iostream>
#include <queue>
using namespace std;
struct Process {
	int name;
	int burst_time;
	int arrival_time;

};
static double ave_turnaround_time = 0;
static double ave_waiting_time = 0;
void swap(Process &p1, Process &p2) {
	Process tmp;
	tmp = p1;
	p1 = p2;
	p2 = tmp;
}

int minBurstTime(Process *p, int n) {
	int min = p[0].burst_time;
	int imin = 0;
	for (int i = 0; i < n; i++)
	{
		if (p[i].burst_time < min) {
			min = p[i].burst_time;
			imin = i;


		}
	}
	return imin;
}

void sortByArrivalTime(Process *p, int n) {
	for (int i = 0; i < n; i++)
	{
		for (int j = i + 1; j < n; j++)
		{
			if (p[i].arrival_time < p[j].arrival_time) {
				swap(p[i], p[j]);
			}
			else {
				if (p[i].arrival_time == p[j].arrival_time) {
					if (p[i].burst_time < p[j].burst_time)
					{
						swap(p[i], p[j]);
					}

				}
			}

		}
	}
}

void ShortestRemainingTimeFirst(Process *p, int n, int time_current, int burst_time) {
	for (int i = 0; i < n - 1; i++)
	{
		for (int j = i + 1; j < n; j++)
		{
			if (p[i].burst_time < p[j].burst_time && p[i].arrival_time <= time_current && p[i].burst_time < burst_time) {
				swap(p[i], p[j]);
			}
		}
	}

}

void Input(Process *p, int n) {
	for (int i = 0; i < n; i++) {
		cout << "-----------------" << endl;
		cout << "Nhap ID process: "; cin >> p[i].name;
		cout << "Nhap burst time: "; cin >> p[i].burst_time;
		cout << "Nhap arrival time: "; cin >> p[i].arrival_time;

	}
}

int check(int flag[], int n) {
	for (int i = 0; i < n; i++) {
		if (flag[i] == 1) return 1;
	}
	return 0;
}

void SelectionFunction(Process *p, int n) {
	Process *p_temp = new Process[100];
	int time_current = 0; 
	///
	int flag_c = 1; 
	int flag_first_come[100]; 
	int flag_previous;
	int flag_current; 
	int waiting_time[100]; 
	for (int i = 0; i < 100; i++) {
		waiting_time[i] = 0;
		flag_first_come[i] = -1; 
									
	}
	sortByArrivalTime(p, n); 
	flag_first_come[p[n - 1].name] = p[n-1].arrival_time;
	while (n > 0) {
		p[n - 1].burst_time--; 
		for (int i = 0; i < n; i++) {
			if (p[i].arrival_time <= time_current) {
				waiting_time[p[i].name]++;
			}
		}
		waiting_time[p[n - 1].name]--;
		if (flag_c == 1) {
			time_current = p[n - 1].arrival_time;
			flag_c = 0;
		}
		time_current++;
		flag_previous = p[n - 1].name; 
		if (p[n - 1].burst_time == 0) {
			cout << p[n - 1].name << "            " << flag_first_come[p[n - 1].name] - p[n-1].arrival_time << "               " << waiting_time[p[n - 1].name] << "            " << (time_current - p[n-1].arrival_time) << endl;
			ave_waiting_time += waiting_time[p[n - 1].name]; 
			ave_turnaround_time += time_current - p[n - 1].arrival_time;	
			n--; 
			if (n == 0) return;
		}		
		ShortestRemainingTimeFirst(p, n, time_current, p[n-1].burst_time); 
		flag_current = p[n - 1].name; 
		if (flag_current != flag_previous) {
			if (flag_first_come[p[n - 1].name] == -1) {
				flag_first_come[p[n - 1].name] = time_current;
			}


		}
	}
}


int main()
{
	Process *p = new Process[100];
	queue<Process> pQueue;
	int n;
	cout << "Nhap so luong process: "; cin >> n;
	Input(p, n);
	cout << "Process   Response-time   Waiting-time   Turn around-time" << endl;

	SelectionFunction(p, n);

	cout << "Thoi gian dap ung trung binh: " << ave_waiting_time / n << endl;
	cout << "Thoi gian hoan thanh trung binh: " << ave_turnaround_time / n << endl;

	system("pause");
	return 0;
}

