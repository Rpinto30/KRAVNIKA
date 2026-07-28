#include <iostream>
#include <string> //string
#include <vector> //vector
#include <cctype> //subtrig, tolower
#include <stack> //stack
#include <algorithm>
#include "logical-connector-lib.h"
#include "json_writte.h"
using namespace std;
using namespace JsonWritter;

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
        result = capitalize_letter & names & numbers;
    }

    Word_json get_word_json(){
        bool special_charts = false;
        if (__context.find("|>;") != string::npos || __context.find("|;") != string::npos || __context.find("||") != string::npos)
        special_charts = true;

        Word_json word(__context, result, init_quotation(), init_hyphen(), contain_name(), 
        there_digits(), special_charts, Logica::OR(Logica::OR(cent_valid(), dec_valid()), thousand_valid()));
        return word;
    }

        bool init_quotation(){
            string new_context = alphaNumeric_mayusc(__context);
            if (new_context.length() < 2) return false; 
            char c = new_context[1];
            if (new_context.substr(2).find('\"') != string::npos) return false;
            return (c == '\"') ? true : false;
        }

        bool init_hyphen(){
            string new_context = alphaNumeric_mayusc(__context);
            if (new_context.length() < 2) return false;
            char c = new_context[1];
            if (new_context.substr(2).find('-') != string::npos) return false;
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
        bool valid_digit_after_special_chart;
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
        bool split_double_dot = false;
        bool end_dot;
        bool last_letter;
        vector<Word> words; 
        bool set_words(){
            string word = "";
            for (size_t index = 0; index < this->__context.length(); index++){
                word += this->__context[index];
                if (this->__context[index] == ':' || this->__context[index] == '.'){ //Cut Phrase
                    split_double_dot = true;
                    end_dot = true;
                    last_letter = true;
                    words.insert(words.end(), Word{word});
                    word = "";
                }
            }
            
            if (!word.empty()) { 
                split_double_dot = false;
                return false;
            }

            bool result_words = 1;
            for (auto word: words){
                bool temp = Logica::AND(result_words, word.get_result());
                result_words = temp;
            }

            bool expression_symbols = false;
            if (__context.find('?') != string::npos && __context.find('!') != string::npos ){
                expression_symbols = Logica::AND(symbol_oc('?'), symbol_oc('!')); //tiene ambas
            } else if (__context.find('?') != string::npos && __context.find('!') == string::npos){
                expression_symbols = symbol_oc('?');
            } else if (__context.find('?') == string::npos && __context.find('!') != string::npos){
                expression_symbols = symbol_oc('!');
            } else{
                expression_symbols = true;
            }
            return Logica::AND(result_words, expression_symbols);
        } 

        bool init_exclamation = false;
        bool close_exclamation = false;
        bool init_interogation = false;
        bool close_interogation = false;
        bool symbol_oc(char open){
            bool added = false;
            stack<char> simbol_stack;
            for(char _ : __context){
                if (!simbol_stack.empty()){
                    if (_ == open) {
                        simbol_stack.pop();
                        
                    }
                    switch(_){
                        case '?': init_interogation = true;
                        break;
                        case '!': init_exclamation = true;
                        break;
                    }
                } else{
                    if (_ == open) {
                        simbol_stack.push(_);
                        added = true;
                        
                    }
                    switch(_){
                        case '?': close_interogation = true;
                        break;
                        case '!': close_exclamation = true;
                        break;
                    }
                }
            }
            
            if (simbol_stack.empty() && added) { return true; }
            return false;
        }

    public:
        Block(string content): __context(content) {
            result_t = set_words();
        } 

        Sentence get_sentence_json(){
            Sentence sentence(__context, result_t, init_exclamation, close_exclamation, 
                init_interogation, close_interogation, split_double_dot, end_dot, last_letter);
            for (auto word : words){
                sentence.set_word(word.get_word_json());
            }
            sentence.close_sentence();
            return sentence;
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


    int set_phrases(){
        string word = "";
        for (size_t index = 0; index < this->context.length(); index++){
            word += this->context[index];
            if (this->context[index] == '.'){ //Cut Phrase
                phrases.insert(phrases.end(), Block{word});
                word = "";
                this->end_dot = true;
                this->last_letter = true;
            }
        }
        
        if (!word.empty()) { 
            this->state = INVALID;
            this->last_letter = false;
            this->end_dot = false;
            phrases.insert(phrases.end(), Block{context});
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
                final_result = false;
            break;
        }
    
        result = final_result;
        if (final_result == true){
            cout<<"1"<<endl;
        } else{
            cout<<"0"<<endl;
        }
    }

    ~Automate(){ delete this; }

    public:
        Automate(string context): context(context),  state(INIT) {
            check_context();
        }
        vector<Block> phrases; 
        string get_context(){ return this->context; }
        bool get_result(){ return result; }
        bool end_dot = false;
        bool last_letter = false;
};

int main(int argc, char* argv[]){
    
    string Cadena;
    if (argc > 1){
        Cadena = argv[1];
    }
    else cin>>Cadena;

    Automate* aut = new Automate(Cadena);
    Json jsonFile(aut->get_result());
    for (auto sentence : aut->phrases){
        jsonFile.set_sentence(sentence.get_sentence_json());
    }
    jsonFile.close_json();
    jsonFile.create_json();

    //string a;
    //cin>>a;
    return aut->get_result();
}
