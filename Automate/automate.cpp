#include <iostream>
#include <string> //string
#include <vector> //vector
#include <cctype> //subtrig, tolower
#include <stack> //stack
#include <algorithm>
#include "logical-connector-lib.h"
using namespace std;


typedef struct Word{
    private:
    string __context;
    bool result;

    string alphaNumeric(string s){
        string t = "";
        for (int i = 0; i < s.length(); i++) {
            if ((s[i] >= 'a' && s[i] <= 'z') || (s[i] >= 'A' && s[i] <= 'Z')) {
                t += tolower(s[i]);
            }
        }
        return t;
    }

    string alphaNumeric_mayusc(string s){
        string t = "";
        for (int i = 0; i < s.length(); i++) {
            if ((s[i] >= 'a' && s[i] <= 'z') || (s[i] >= 'A' && s[i] <= 'Z') || s[i] == '\"'|| s[i] == '-') {
                t += tolower(s[i]);
            }
        }
        return t;
    }

    public:
    Word(string content) : __context(content) {
        bool capitalize_letter = Logica::XOR(init_quotation(), init_hyphen());
        bool names = Logica::NOT(contain_name());
        bool numbers = Logica::IMPLIES(
            Logica::OR(Logica::OR(cent_valid(), dec_valid()), thousand_valid())
            ,there_digits());

        cout<<"------"<<__context<<"------"<<endl;
        cout<<"Mayuscula: "<<capitalize_letter<<endl;
        cout<<"Nombres: "<<names<<endl;
        cout<<"Numeros: "<<numbers<<endl;
     

        result = capitalize_letter & names & numbers;
    }

        bool init_quotation(){
            char c = alphaNumeric_mayusc(__context)[1];
            if (alphaNumeric_mayusc(__context).substr(2).find('\"') != string::npos) return false;
            return (c == '\"') ? true : false;
        }

        bool init_hyphen(){
            char c = alphaNumeric_mayusc(__context)[1];
            if (alphaNumeric_mayusc(__context).substr(2).find('-') != string::npos) return false;
            return (c == '-') ? true : false;
        }

        bool contain_name(){
            string names[] = {"jorge", "jhonathan", "fabritzio", "rodrigo"};
            string alpha_numeric_context = alphaNumeric(__context);
            for(string name : names){
                if (alpha_numeric_context.find(name) != string::npos) return true;
            }
           
            return false;
        }

        bool there_digits(){
            return any_of(__context.begin(), __context.end(), ::isdigit);
        }

        // NUMEROS
        bool thousand_valid(){
            size_t index_thousand = 0;
            string sub_thousand = __context;
            bool valid = false;
            do {
                index_thousand = sub_thousand.find("|>;");
                if (index_thousand == string::npos) break;
                
                char thousand = sub_thousand[index_thousand+3];
                if (thousand >= '1' && thousand <= '9') valid = true;
                else valid = false;

                string temp = sub_thousand.substr(index_thousand+3);
                sub_thousand = temp;
            } while(index_thousand != string::npos);

            return valid;
        }

        bool cent_valid(){
            size_t index_cent = 0;
            string sub_cent = __context;
            bool valid = false;
            do {
                index_cent = sub_cent.find("|;");
                if (index_cent == string::npos) break;
                
                char cent = sub_cent[index_cent+2];
                if (cent >= '1' && cent <= '9') valid = true;
                else valid = false;

                string temp = sub_cent.substr(index_cent+2);
                sub_cent = temp;
            } while(index_cent != string::npos);

            return valid;
        }

        bool dec_valid(){
            size_t index_dec = 0;
            string sub_dec = __context;
            bool valid = false;
            do {
                index_dec = sub_dec.find("||");
                if (index_dec == string::npos) break;
                
                char dec = sub_dec[index_dec+2];
                if (dec >= '1' && dec <= '9') valid = true;
                else valid = false;

                string temp = sub_dec.substr(index_dec+2);
                sub_dec = temp;
            } while(index_dec != string::npos);

            return valid;
        }

    string get_context() { return __context; }
    bool get_result() { return result; }
} Word;


typedef struct Block{
    private:
        string __context;
        size_t result_t;

        //VALID WORDS
        vector<Word> words; 
        bool set_words(){
            string word = "";
            for (size_t index = 0; index < this->__context.length(); index++){
                word += this->__context[index];
                if (this->__context[index] == ':' || this->__context[index] == '.'){ //Cut Phrase
                    words.insert(words.end(), Word{word});
                    word = "";
                }
            }
            
            if (!word.empty()) { 
                return false;
            }

            bool result_words = 1;
            for (auto word: words){
                bool temp = Logica::AND(result_words, word.get_result());
                result_words = temp;
            }

            bool expression_symbols = Logica::OR(symbol_oc('?'), symbol_oc('!'));
            return Logica::AND(result_words, expression_symbols);
        } 

        bool symbol_oc(char open){
            stack<char> simbol_stack;
            cout<<__context;
            for(char _ : __context){
                
                if (!simbol_stack.empty()){
                    if (_ == open) simbol_stack.pop();
                } else{
                    if (_ == open) simbol_stack.push(_);
                }
            }
            
            if (simbol_stack.empty()) { return true; }
            
            return false;
        }

    public:
        Block(string content): __context(content) {
            result_t = set_words();
        } 

        int get_result() { return result_t; }
        string get_context() { return __context; }

} Block;

class Automate{
    private:
    string context;
    enum STATE { INIT, PHRASE, WORD, INVALID };
    STATE state;
    bool result = false; 
    
    //Only call when state == INVALID
    void invalid_action(){
        cout<<"Cadena no valida"<<endl;
    }

    vector<Block> phrases; 
    int set_phrases(){
        string word = "";
        for (size_t index = 0; index < this->context.length(); index++){
            word += this->context[index];
            if (this->context[index] == '.'){ //Cut Phrase
                phrases.insert(phrases.end(), Block{word});
                word = "";
            }
        }
        
        if (!word.empty()) { 
            this->state = INVALID;
            return 0;
        }
        this->state = PHRASE;
        return 1;
    }

    
    void check_context(){
        set_phrases();
        bool final_result = true;    
        switch(state){
            case PHRASE:  
                for (auto block : phrases){
                    bool temp = Logica::AND(final_result, block.get_result());
                    final_result = temp;
                }
            break;
            case INVALID:
                invalid_action();
            break;
        }
    
        result = final_result;
        if (final_result == true){
            cout<<endl<<endl;
            cout<<"LA CADENA INTRODUCIDA ES VALIDA"<<endl;
        } else{
            cout<<endl<<endl;
            cout<<"LA CADENA INTRODUCIDA NO ES VALIDA"<<endl;
        }
    }


    ~Automate(){ delete this; }

    public:
        Automate(string context): context(context),  state(INIT) {
            check_context();
        }

        string get_context(){ return this->context; }
        bool get_result(){ return result; }
};

int main(int argc, char* argv[]){
    
    string Cadena;
    if (argc > 1){
        Cadena = argv[1];
    }
    else cin>>Cadena;

    // if (Cadena == "a") Cadena = "N\"ACI:E\"L:A\"NIO|>;27+|>;5||12.H-OLA:ESTO:E-S:UNA:P\"RUE\"BA.ES\"TA:E-\"S:L\"A:T-\"ERCERA:FR|>;51ASE.M-e:l\"lamo:rodrigo235.";
    Automate* aut = new Automate(Cadena);
    string a;

    //cout<<aut->get_context()<<endl;
    
    return aut->get_result();
}
// TODO
// convertir en tokens 
// realizar separacion de oracion segun temine con . solo si es el ultimo caracter - EN GENERAL (LIIIIIIIIIIIIIIIIIIIIIIIIIIISTO)
// por cada frase:
//  -separacion de palabras segun inicie con (" o ') y termine con (: si no es el ultimo caracter) - EN ORACION
//  para todos los tokens realizar la verificacion:
//      - verificar existencia de nombres dentro del token - EN PALABRA
//      - verificar signos de apertura y cierre - EN PALABRA
//      - verificar si hay numeros en la palabra - EN PALABRA