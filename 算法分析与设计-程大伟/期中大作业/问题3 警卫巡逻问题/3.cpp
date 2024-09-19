#include <iostream>
#include <cmath>
#include <algorithm>
#include <vector>
using namespace std;

// 存储节点的信息
struct node {
    // 坐标
    int x, y;
    // 节点名称
    char id;
};

class Solution {
private:
    // 结点个数
    int n;
    // 结点信息
    vector<node> nodeList;
    // 记录组成的三角形信息
    vector<vector<int> > s;

    // 求两点的欧氏距离
    double getEucDistance(int i, int j)
    {
        return sqrt((nodeList[i].x - nodeList[j].x) * (nodeList[i].x - nodeList[j].x) + (nodeList[i].y - nodeList[j].y) * (nodeList[i].y - nodeList[j].y));
    }

public:
    // 初始化 输入信息
    void init()
    {
        cin >> n;

        s.resize(n);
        for (int i = 0; i < n; i++)
            s[i].resize(n);
        
        for (int i = 0; i < n; i++) {
            node element;
            cin >> element.id >> element.x >> element.y;
            nodeList.push_back(element);
        }
    }

    // 求算最小警卫巡逻成本
    double getLowestCost()
    {
        // dp[i][j] 表示凸多边形从 i 到 j 最小的警卫巡逻成本
        vector<vector<double> > dp(n, vector<double>(n, 0));

        // r 为 j 与 i 的差值
        for (int r = 2; r <= n; r++) {
            for (int i = 0; i < n - r; i++) {
                int j = i + r;
                dp[i][j] = INFINITY;
                // k 在 i 到 j 滑动
                for (int k = i + 1; k < j; k++) {
                    double u = dp[i][k] + getEucDistance(i, k) + getEucDistance(k, j) + getEucDistance(i, j) + dp[k][j];
                    if (u < dp[i][j]) {
                        dp[i][j] = u;
                        // 存储划分方案
                        s[i][j] = k;
                    }
                }
            }
        }

        return dp[0][n - 1];
    }

    // 输出警卫巡逻路线方案
    void printSolution()
    {
        vector<pair<int, int> > solutionList;
        solutionList.push_back({ 0, n - 1 });
        while (solutionList.size()) {
            pair<int, int> cur = solutionList.back();
            solutionList.pop_back();
            // 已经到了终止的情况
            if (cur.first + 1 == cur.second)
                continue;
            cout << nodeList[cur.first].id << nodeList[cur.second].id << nodeList[s[cur.first][cur.second]].id << endl;
            solutionList.push_back({ cur.first, s[cur.first][cur.second] });
            solutionList.push_back({ s[cur.first][cur.second], cur.second });
        }
    }
};


int main()
{

    Solution s;
    s.init();
    cout << s.getLowestCost() << endl;
    s.printSolution();

    return 0;
}

