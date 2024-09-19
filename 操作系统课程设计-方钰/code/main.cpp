#include <iostream>
#include "OSKernel.h"
#include "Shell.h"
using namespace std;

int main()
{
	OSKernel& o = OSKernel::Instance();

	Shell s;
	s.interface();

	return 0;
}