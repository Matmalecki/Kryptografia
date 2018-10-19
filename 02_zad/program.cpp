#include <iostream>
#include <fstream>
#include "string.h"

const int lengthOfLine = 4;

using namespace std;
void MakePlainText();


int main()
{
	MakePlainText();
	
	
	return 0;
}

void MakePlainText()
{
	ifstream input;
	input.open("orig.txt");
	ofstream output;
	output.open("plain.txt");
	
	char ch;
	if (input.is_open())
	{
		int i = 0;
		while (input >> ch) {
			output << ch; // Or whatever
			i++;
			if (i==lengthOfLine)
			{
				i=0;
				output << '\n';
			}
		}
	}
}

