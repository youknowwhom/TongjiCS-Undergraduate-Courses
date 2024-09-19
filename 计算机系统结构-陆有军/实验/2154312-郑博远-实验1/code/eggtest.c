#define _CRT_SECURE_NO_WARNINGS
#include <stdio.h>

int main()
{
	int init_floor;
	int init_resistance;

	printf("请输入楼层数：");
	scanf("%d", &init_floor);

	printf("请输入耐摔值：");
	scanf("%d", &init_resistance);

	int result_attempt_cnt = 0;
	int result_broken_cnt  = 0;
	bool result_is_last_broken = 0;

	int l = 0, r = init_floor;

	while (l < r){

		result_attempt_cnt++;

		int mid = (l + r + 1) / 2;

		if (mid > init_resistance){
			result_is_last_broken = 1;
			r = mid - 1;
			result_broken_cnt ++;
		}
		else{
			result_is_last_broken = 0;
			l = mid;
		}
		printf("进行第%d次实验, 在%d层扔鸡蛋, 本次鸡蛋", result_attempt_cnt, mid);
		printf(result_is_last_broken ? "摔碎\n" : "没碎\n");
	}

	printf("共尝试%d次，摔碎鸡蛋%d个，最后一次鸡蛋", result_attempt_cnt, result_broken_cnt );
	printf((result_is_last_broken ? "摔碎\n" : "没碎\n"));

	return 0;
}
