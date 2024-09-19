int a;
float b;

float sum(int a, float b){
  float c;
  c = a + b;
  if(c > 2.1){
    return c;
  }
  else{
    return 0 - c;
  }
}

int main(){
  int n;
  float ans;

  n = 10;
  ans = 0;

  while (n > 0){
    n = n - 1;
    ans = ans + sum(n, 1.2);
  }

  return 0;
}