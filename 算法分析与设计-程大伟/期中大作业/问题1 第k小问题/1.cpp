#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <ctime>

using namespace std;

// 表示输入数据的数据类型
// 说明：由于三种算法方式不同，当数字大小相同时不会选择相同的字母；为方便观察，在比较大小时若数字相同，则进一步以字母的ASCII码作为比较依据
struct ElemType {
	int num;
	char letter;

	bool operator< (const ElemType& that) const
	{
		// 选择算法不是稳定的
		// 在数字相同的前提下比较字母能够让三个答案相同 方便观察
		if (num == that.num)
			return letter < that.letter;
		return num < that.num;
	}

	bool operator> (const ElemType& that) const
	{
		if (num == that.num)
			return letter > that.letter;
		return num > that.num;
	}
};

class Solve {
private:
	// 将 nums[l] 排位到正确的位置上
	int partition(vector<ElemType>& nums, int l, int r)
	{
		int i = l - 1, j = r + 1;

		ElemType x = nums[l];
		while (true) {
			while (nums[++i] < x && i < r)
				;
			while (nums[--j] > x)
				;
			if (i >= j)
				break;

			swap(nums[i], nums[j]);
		}

		return j;
	}

	// 函数重载 用于方法3
	int partition(vector<ElemType>& nums, int l, int r, ElemType x)
	{
		int i = l - 1, j = r + 1;

		while (true) {
			while (nums[++i] < x && i < r)
				;
			while (nums[--j] > x)
				;
			if (i >= j)
				break;

			swap(nums[i], nums[j]);
		}

		return j;
	}

	int randomizedPartition(vector<ElemType>& nums, int l, int r)
	{
		// 随机选择一个数
		int i = rand() % (r - l + 1) + l;
		swap(nums[l], nums[i]);
		return partition(nums, l, r);
	}

	// 二分递归的部分
	ElemType randomizedSelect(vector<ElemType>& nums, int l, int r, int k)
	{
		if (l == r)
			return nums[l];
		int i = randomizedPartition(nums, l, r);
		// j 表示 i 在序列 l 到 r 中是第 j 大
		int j = i - l + 1;
		
		if (k <= j)
			return randomizedSelect(nums, l, i, k);
		else
			return randomizedSelect(nums, i + 1, r, k - j);
	}


	// 选择中位数做枢纽的版本
	ElemType medianSelect(vector<ElemType>& arr, int l, int r, int k)
	{
		
		// 队列足够短 直接排序找结果
		if (r - l < 75) {
			// 冒泡排序
			sort(arr.begin() + l, arr.begin() + r + 1);
			return arr[l + k - 1];
		}

		for (int i = 0; i <= (r - l - 4) / 5; i++) {
			// 排序找中位数
			sort(arr.begin() + l + 5 * i, arr.begin() + l + 5 * i + 4);
			// 找到中位数交换到队列头
			swap(arr[l + i], arr[l + 5 * i + 2]);
		}

		// 继续递归找中位数的中位数
		ElemType x = medianSelect(arr, l, l + (r - l - 4) / 5, (r - l - 4) / 10);

		int i = partition(arr, l, r, x);

		int j = i - l + 1;

		if (k <= j)
			return medianSelect(arr, l, i, k);
		else
			return medianSelect(arr, i + 1, r, k - j);
	}

public:
	// 方法1 通过堆实现
	ElemType solve1_heap(vector<ElemType> nums, int k)
	{
		// 对前 k 个数建立一个大根堆，时间复杂度为 O(k)
		make_heap(nums.begin(), nums.begin() + k);

		// 对于之后的数，不断维护大根堆；时间复杂度为 O((n-k)logk)
		for (int i = k; i < (int)nums.size(); i++) {
			// 若大于堆顶元素则跳过
			if (nums[i] > nums[0])
				continue;
			// 更新堆
			pop_heap(nums.begin(), nums.begin() + k);
			nums[k - 1] = nums[i];
			push_heap(nums.begin(), nums.begin() + k);
		}
		return nums[0];
	}

	// 方法2 随机划分线性选择
	ElemType solve2_randomized(vector<ElemType> nums, int k)
	{
		return randomizedSelect(nums, 0, nums.size() - 1, k);
	}

	// 方法3 中位数划分选择
	ElemType solve3_median(vector<ElemType> nums, int k)
	{
		return medianSelect(nums, 0, nums.size() - 1, k);
	}

};

int main()
{
	Solve s;
	int n, k;
	time_t t_start, t_end;
	vector<ElemType> nums;

	srand((unsigned)time(nullptr));

	for (int j = 1; j <= 10; j++) {
		// 从测试样例中读入的正确答案
		ElemType answer;
		// 从文件读
		ifstream infile("in" + to_string(j) + ".txt", ios::in);		// in.txt 存测试样例的输入信息
		ifstream infile2("out" + to_string(j) + ".txt", ios::in);	// out.txt 存测试样例的输出信息(正确答案)
		if (!infile.is_open() || !infile2.is_open())
			return 0;
		infile >> n >> k;
		nums.clear();
		for (int i = 0; i < n; i++) {
			ElemType e;
			infile >> e.letter >> e.num;
			nums.push_back(e);
		}
		infile2 >> answer.letter >> answer.num;

		infile.close();
		infile2.close();

		cout << "-- 下面测试第" << j << "组测试数据 --" << endl;
		cout << "正确答案是 : " << answer.letter << " " << answer.num << endl;


		// 把结果写入到文件
		for (int i = 1; i <= 3; i++) {
			string outfilename = "out" + to_string(j) + "_solution" + to_string(i) + ".txt";
			ofstream outfile(outfilename, ios::out);
			if (!outfile.is_open())
				return 0;
			t_start = clock();
			ElemType newans;
			switch (i) {
				case 1:
					newans = s.solve1_heap(nums, k);
					break;
				case 2:
					newans = s.solve2_randomized(nums, k);
					break;
				case 3:
					newans = s.solve3_median(nums, k);
					break;
			}
			t_end = clock();
			outfile << newans.letter << " " << newans.num;
			cout << "方法" << i << "得到答案 : " << newans.letter << " " << newans.num << ", 耗时" << double(t_end - t_start) / CLOCKS_PER_SEC << "s" << endl;
			outfile.close();

		}
		cout << endl << endl;
	}
		
	return 0;
}