#include <iostream>
#include <string>
#include <vector>
#include <memory>
using namespace std;

int global_id = 1;
typedef struct Block{
    private:
        int id;
        string __content;
        int token;

    public:
        Block(string content): __content(content) {
            id = global_id++;
            token = 0; // False
        } 

        int get_id() { return id; }
        int get_token() { return token; }
        string get_content() { return __content; }

} Block;

vector<string> tokenizar(const string& content) {
    vector<string> tokens;
    tokens.reserve(content.size() / 4);

    const char* p   = content.data();
    const char* end = p + content.size();

    while (p < end) {
        if (isalnum((unsigned char)*p) || *p == '_') {
            const char* start = p;
            while (p < end && (isalnum((unsigned char)*p) || *p == '_'))
                ++p;
            tokens.emplace_back(start, p);
        } else if (*p == ':' || *p == ',' || *p == ';') {
            tokens.emplace_back(p, 1);
            ++p;
        } else {
            ++p;
        }
    }
    return tokens;
}


int main(){
    cout<<"Hola mundo"<<endl;
    string s = "UserA:4,3;UserB:1;UserC:2;";
    string a;

    vector<unique_ptr<Block>> list;
    list.push_back(make_unique<Block>(Block{"Este es el contenido"}));
    list.push_back(make_unique<Block>(Block{"Este es el contenido 2"}));
    list.push_back(make_unique<Block>(Block{"Este es el contenido 3"}));
    for (const auto s : tokenizar(s)) {
        cout<<s<<endl;
        //cout << p->get_content() << " | " << p->get_id() <<endl;
    } 
    cin>>a;

    return 0;
}

// TODO
// convertir en tokens
// realizar separacion de oracion segun temine con . solo si es el ultimo caracter - EN GENERAL
// por cada frase:
//  -separacion de palabras segun inicie con (" o ') y termine con (: si no es el ultimo caracter) - EN ORACION
//  para todos los tokens realizar la verificacion:
//      - verificar existencia de nombres dentro del token - EN PALABRA
//      - verificar signos de apertura y cierre - EN PALABRA
//      - verificar si hay numeros en la palabra - EN PALABRA