#include<bits/stdc++.h>
#include <string>
#include <regex>
using namespace std;

vector<string> name;
vector<string> type;
vector<int> location;
vector<int> s;

map<string,int> mot, dir;
string label, opcode;

void init() //directive Table(dir) And Machine instruction(mot) code Table
{

	mot.insert(pair<string,int>("MOV",4));
	mot.insert(pair<string,int>("ADD",8));
	mot.insert(pair<string,int>("JMP",4));
	mot.insert(pair<string,int>("CLC",2));

	dir.insert(pair<string,int>("SEGMENT",0));
	dir.insert(pair<string,int>("END",0));
	dir.insert(pair<string,int>("DB",1));
	dir.insert(pair<string,int>("DW",2));
}

void decodeInst(string inst){

	label = "";
	opcode = "";

	int idx = 0, strtIdx;

	while(inst[idx] != '\0' && (inst[idx] == ' ' || inst[idx] == '\t')) idx++; // space handling

	strtIdx = idx;

	while(inst[idx] != '\0') // read until end
	{
		if(inst[idx] == ':'){
			label = inst.substr(strtIdx, idx - strtIdx);
			break;
		}else if(inst[idx] == ' '){
			opcode = inst.substr(strtIdx, idx - strtIdx);
			break;
		}
		idx++;
	}

	idx++;
	while(inst[idx] != '\0' && (inst[idx] == ' ' || inst[idx] == '\t'))idx++; // space handling

	strtIdx = idx;

	if(label != ""){
		while(inst[idx] != '\0')
		{
			if(inst[idx] == ' ')
			{
                opcode = inst.substr(strtIdx, idx-strtIdx);
                break;
			}
			idx++;
		}

		if(opcode == "")
		{
			opcode = inst.substr(strtIdx);
		}
	}

}

int main()
{

  init();
  ifstream in("code.txt"); // in - file hndler

  if(!in) {
    cout << "Cannot open input file.\n";
    return 1;
  }

  string str;

  int lc = 0;

  map<string, int>::iterator it1, it2;
  vector<string>::iterator it3;

  while(getline(in, str)) {

	if(regex_match (str, regex("[\n\t ]+") )){
    	continue;
	}

    decodeInst(str);

    if(label != ""){
        it3 = find(name.begin(), name.end(), label);
        if(it3 != name.end()){
            cout << "PASS1 Failed Variable found" << endl;
            break;
        }else{
            name.push_back(label);
            type.push_back("label");
            location.push_back(lc);
            s.push_back(0);
        }
    }

    it1 = mot.find(opcode);
    it2 = dir.find(opcode);

    if(it1 != mot.end()){
        lc += it1->second;
    }else if(it2 != dir.end()){
        if(opcode == "END"){
            cout << "PASS1 Complete END" << endl;
            break;
        }else if(opcode == "SEGMENT"){
            lc = 0;
            it3 = find(name.begin(), name.end(), label);
            int index = distance( name.begin(), it3 );
            type[index] = "SEGMENT";
        }else{
            it3 = find(name.begin(), name.end(), label);
            int index = distance( name.begin(), it3 );
            type[index] = opcode;
            s[index] = it2->second;
            lc += it2->second;
        }
    }else if(opcode == ""){
    	continue;
    }else{
    	cout << "PASS 1 Failed SYNTAX ERROR" << endl;
        break;
    }

  }

  cout << "SYMBOL TABLE" << endl;

  cout <<"\t Name\tType\tLocation Counter\tSize " << endl;

  for(int i = 0; i < name.size(); i++){

	cout<<"\n";
    cout <<"\t"<<name[i] << "\t" << type[i] << "\t\t" << location[i] << "\t\t" << s[i] << endl;
  }

  in.close();

  return 0;
}
