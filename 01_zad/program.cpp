#include <iostream>
#include <fstream>
#include "string.h"
using namespace std;

void CryptAfin();
void DecryptAfin(int k, int a);
char ShiftLetterAfin(char l, int num, int factor);
void KAallAfin();
void KAAfin();

void CryptCezar();
void DecryptCezar(int k);
char ShiftLetterCezar(char l, int num);
void KACezar();
void KAallCezar();

int KeyShift();
int KeyFactor();

int NWD(int a, int b)
{
  int c;
	while(b!=0)
    {
		c = b;
		b = a%b;
		a = c;
	}
  return a;
}
int Odwrotnosc(int a)
{
  int m = 26;
  a=a%m;
  for (int i=1; i<m; i++)
    if ((a*i) % m == 1)
      return i;
  return -1;
}


void PrintHelp();

int main(int argc, char * argv[])
{
  if (argc > 2){
    if (!strcmp(argv[1],"-c"))
    {
      //cezar
        if (!strcmp(argv[2],"-e"))
          if (KeyShift() != -1)
            CryptCezar();
          else cout << "Brak klucza w pliku" << endl;
        else if(!strcmp(argv[2],"-d"))
          if (KeyShift() != -1)
          DecryptCezar(KeyShift());
          else cout << "Brak klucza w pliku" << endl;
        else if (!strcmp(argv[2],"-j"))
           KACezar();
        else if (!strcmp(argv[2],"-k"))
          KAallCezar();
    }
    else if  (!strcmp(argv[1],"-a"))
    {
      if (!strcmp(argv[2],"-e"))
        if (KeyShift() != -1 && KeyFactor() != -1)
          CryptAfin();
        else cout << "Brak klucza w pliku" << endl;
      else if(!strcmp(argv[2],"-d"))
        if (KeyShift() != -1 && KeyFactor() != -1)
          DecryptAfin(KeyShift(), KeyFactor());
        else cout << "Brak klucza w pliku" << endl;
      else if (!strcmp(argv[2],"-j"))
         KAAfin();
      else if (!strcmp(argv[2],"-k"))
        KAallAfin();
    }
    else PrintHelp();
  }
  else PrintHelp();

  return 0;
}

void CryptAfin(){
  ifstream input;
  input.open("plain.txt");
  ofstream output;
  output.open("crypto.txt");
  string line;
  if (input.is_open() && output.is_open())
  {
    for( string line; getline( input, line ); )
    {
      for (int i = 0; i < line.size(); i++){
          output << ShiftLetterAfin(line[i], KeyShift(), KeyFactor());
      }
      output << endl;
    }

  }
  else cout << "Brak plikow" << endl;

  input.close();
  output.close();

}
void DecryptAfin(int k, int a){
  ifstream input;
  input.open("crypto.txt");
  ofstream output;
  output.open("decrypt.txt");
  string line;
  if (input.is_open() && output.is_open())
  {
    for( string line; getline( input, line ); )
    {
      for (int i = 0; i < line.size(); i++){
          output << ShiftLetterAfin(line[i], -k, Odwrotnosc(a));
      }
      output << endl;
    }

  }
  else cout << "Brak plikow" << endl;

  input.close();
  output.close();



}
char ShiftLetterAfin(char l, int num, int factor){

  int letter = l;
  if (letter <='Z' && letter >='A')
  {
      letter = letter - 'A';
      if (num < 0)
      {
        letter+=num;
        letter*=factor;
      } else {
        letter*=factor;
        letter+=num;
      }
    if (letter >=0)
        letter%=26;
      else letter = ( letter % 26 ) + 26;
      letter += 'A';
      return letter;
  } else if (letter <='z' && letter >='a')
  {
    letter = letter - 'a';
    if (num < 0)
    {
      letter+=num;
      letter*=factor;
    } else {
      letter*=factor;
      letter+=num;
    }
    if (letter >=0)
      letter%=26;
    else letter = ( letter % 26 ) + 26;
    letter += 'a';
    return letter;
  }
  else return letter;

}
void KAallAfin(){
  ifstream input;
  input.open("crypto.txt");
  if (input.is_open())
  {
    for (int a = 1; a < 26; a++)
    {
      if (NWD(a,26)==1 && Odwrotnosc(a) != -1)
      {
          for (int k = 1; k <= 26; k++)
          {
            for( string line; getline( input, line ); )
            {
              for (int i = 0; i < line.size(); i++){
                  cout << ShiftLetterAfin(line[i], k, Odwrotnosc(a));
              }
              cout << endl;
            }
            input.clear();
            input.seekg(0, ios::beg);
          }
        }
      }

    }

}
void KAAfin(){
  ifstream inputCrypto;
  inputCrypto.open("crypto.txt");
  ofstream outputKey;
  outputKey.open("key-new.txt");
  ifstream inputSource;
  inputSource.open("extra.txt");

  string lineCrypto;
  getline(inputCrypto, lineCrypto);
  string lineSource;
  getline(inputSource, lineSource);
  bool success = false;
  int k = 0;
  int a = 0;
  for (a = 1; a < 26; a++)
  {
    if (NWD(a,26)==1 && Odwrotnosc(a) != -1)
    {
        for (k=0;k<26;k++)
        {
            if (lineCrypto[0] == ShiftLetterAfin(lineSource[0], k, Odwrotnosc(a)) && lineCrypto[1] == ShiftLetterAfin(lineSource[1], k, Odwrotnosc(a)))
            {
              success = true;
              break;
            }
        }
    }
    if (success) {
      break;
    }
  }

  if (success)
  {
    outputKey << k << " " << Odwrotnosc(a);
    DecryptAfin(k, Odwrotnosc(a));
  } else cout << "Blad! Brak rozwiazania!"<< endl;

}

void CryptCezar(){
  ifstream input;
  input.open("plain.txt");
  ofstream output;
  output.open("crypto.txt");
  string line;
  if (input.is_open() && output.is_open())
  {
    for( string line; getline( input, line ); )
    {
      for (int i = 0; i < line.size(); i++){
          output << ShiftLetterCezar(line[i], KeyShift());
      }
      output << endl;
    }

  }
  else cout << "Brak plikow" << endl;

  input.close();
  output.close();
}
char ShiftLetterCezar(char l, int num){
  int letter = l;
  if (letter <='Z' && letter >='A')
  {
      letter = letter - 'A';
      letter+=num;
      if (letter >=0)
        letter%=26;
      else letter = ( letter % 26 ) + 26;
      letter += 'A';
      return letter;
  } else if (letter <='z' && letter >='a')
  {
    letter = letter - 'a';
    letter+=num;
    if (letter >=0)
      letter%=26;
    else letter = ( letter % 26 ) + 26;
    letter += 'a';
    return letter;
  }
  else return letter;

}
void KAallCezar(){
  ifstream input;
  input.open("crypto.txt");
  if (input.is_open())
  {
    for (int k = 1; k < 26; k++)
    {
      for( string line; getline( input, line ); )
      {
        for (int i = 0; i < line.size(); i++){
            cout << ShiftLetterCezar(line[i], k);
        }
        cout << endl;
      }
      input.clear();
      input.seekg(0, ios::beg);
    }
  }


}
void KACezar(){
  ifstream inputCrypto;
  inputCrypto.open("crypto.txt");
  ofstream outputKey;
  outputKey.open("key-new.txt");
  ifstream inputSource;
  inputSource.open("extra.txt");
  char firstletterSource;
  char firstletterCrypto;
  string line;
  getline(inputCrypto, line);
  firstletterCrypto = line[0];
  getline(inputSource, line);
  firstletterSource = line[0];
  bool success = false;
  int k = 0;
  for (k=0;k<26;k++)
  {
    if (firstletterCrypto == ShiftLetterCezar(firstletterSource, k))
    {
      success = true;
      break;
    }

  }
  if (success)
  {
    outputKey << k;
    DecryptCezar(k);
  } else cout << "Blad! Brak rozwiazania!"<< endl;


}
void DecryptCezar(int k){
  ifstream input;
  input.open("crypto.txt");
  ofstream output;
  output.open("decrypt.txt");
  string line;
  if (input.is_open() && output.is_open())
  {
    for( string line; getline( input, line ); )
    {
      for (int i = 0; i < line.size(); i++){
          output << ShiftLetterCezar(line[i], -k);
      }
      output << endl;
    }

  }
  else cout << "Brak plikow" << endl;

  input.close();
  output.close();

}


int KeyShift(){
  ifstream input;
  input.open("key.txt");
  if (input.is_open()){
    int n;
    input >> n;
    if (n <= 0 || n >= 26)
      return -1;
    return n;
  }
  return -1;
}
int KeyFactor(){
  ifstream input;
  input.open("key.txt");
  if (input.is_open()){
    int n;
    input >> n;
    input >> n;
    if (NWD(n,26)!=1 || n < 0 || n > 26)
      return -1;
    return n;
  }
  return -1;
}
void PrintHelp(){
  cout << "Brak argumentow" << endl;
  cout << "-c (szyfr Cezara), Pierwszy arg" << endl;
  cout << "-a (szyfr afiniczny), Pierwszy arg" << endl;
  cout << "-e (szyfrowanie), Drugi arg" << endl;
  cout << "-d (odszyfrowywanie), Drugi arg" << endl;
  cout << "-j (kryptoanaliza z tekstem jawnym), Drugi arg" << endl;
  cout << "-k (kryptoanaliza wylacznie w oparciu o kryptogram), Drugi arg" << endl;
}
