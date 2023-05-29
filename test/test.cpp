
#include <iostream>
#include <string>
 
using namespace std;
class Animals
{
public:
	virtual void Bark()
	{
		cout << "动物叫声" << endl;
	}
};
class Cat :public Animals
{
public:
	virtual void Bark()
	{
		cout << "喵喵喵" << endl;
	}
};
void Barking(Animals& animals)
{
	animals.Bark();
}
void text()
{
	Cat cat;
	Barking(cat);
}
 
int main()
{
	text();
}
