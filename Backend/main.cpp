#include <iostream>
#include "bookTables.cpp"
#include "stock.cpp"
#include "foodQueue.cpp"

using namespace std;

bookTables t = bookTables(5);
Stock s;
foodQueue q;

void initComponent(){
    s.importfile("test.txt");
}

int main(){
    string mode;
    string text;

    initComponent();

    while (true){
        cout << "Select mode (book, stock, queue, exit) : ";
        cin >> mode;
        if (mode == "book"){
            while (true){
                cout << "Enter a command (book, clear, checkBookTable, checkUnbookTable, display, menu): ";
                cin >> text;

                if (text == "book"){
                    int x;
                    cout << "Enter the table number to book: ";
                    cin >> x;
                    if ( x > t.getSize() or x == 0){
                        cout << "No that table number" << endl;
                    }
                    else{
                        t.books(x);
                    }
                }
                else if (text == "clear"){
                    int x;
                    cout << "Enter the table number to clear: ";
                    cin >> x;
                    if( x > t.getSize() or x == 0){
                        cout << "No that table number" << endl;
                    }
                    else{
                        t.clear(x);
                    }
                }
                else if(text == "checkBookTable"){
                    t.checkbookTable();
                }

                else if (text == "checkUnbookTable"){
                    t.checkunbookTable();
                }
                else if (text == "display"){
                    t.display();
                }
                else if (text == "menu"){
                    break;
                }
            }
        }

        if (mode == "stock"){
            while (true){
                cout << "Enter a command (addStock, delStock, updateStock checkStock, searchStock, exportfile, display, menu) : " << endl;
                cin >>  text;
                if (text == "addStock"){
                    string name;
                    int value;
                    cout << "What do you want to add : ";
                    cin >> name;
                    if (s.search(name) != -1){
                        cout << "That menu is already exist" << endl;
                    }
                    else{
                        cout << "How many do you add : ";
                        cin >> value;
                        s.insert(name,value);
                        cout << "Add Success!!"<<endl;
                    }
                }

                else if (text == "delStock"){
                    string name;
                    int value;
                    cout << "What do you want to delete : ";
                    cin >> name;
                    if (s.search(name) == -1){
                        cout << "Don't have that menu in the stock" << endl;
                    }
                    else{
                        s.del(name);
                        cout << "Delete Success!!"<<endl;
                    }
                }

                else if (text == "updateStock"){
                    string name;
                    int value;
                    cout << "What do you want to update : ";
                    cin >> name;
                    if (s.search(name) == -1){
                        cout << "Don't have that menu in the stock" << endl;
                    }
                    else{
                        cout << "How many do you update : ";
                        cin >> value;
                        s.setValue(name,value);
                        cout << "Update Success!!"<<endl;
                    }
                }

                else if (text == "checkStock"){
                    s.stockcheck();
                }
                
                else if (text == "searchStock"){
                    string name;
                    cout << "What food do you want to check? : ";
                    cin >> name;
                    if (s.search(name) == -1){
                        cout << "Don't have that menu in the stock" << endl;
                    }
                    else{
                        cout << name << " : " << s.getValue(name) << endl;
                    }
                }

                else if (text == "exportfile"){
                    s.exportfile();
                }
                else if (text == "display"){
                    s.display();
                }
                else if (text == "menu"){
                    break;
                }
            }
        }

        if (mode == "queue"){

            while (true){
                cout << "Enter a command (enqueue, dequeue, checkQueue, display, menu) : ";
                cin >>  text;

                if (text == "enqueue"){
                    int table;
                    string menu;
                    int number;
                    cout << "Table : ";
                    cin >> table;
                    if(t.getValue(table-1) == 0){
                        cout << " This table isn't booked yet" << endl;
                    }
                    else{
                        cout << "Menu : ";
                        cin >> menu;
                        if(s.search(menu) == -1){
                            cout <<  "We don't have that menu" <<endl;
                        }
                        else{
                            cout << "Number :";
                            cin >> number;
                            if (s.getValue(menu) < number){
                                cout << "That menu doesnt have enough" <<endl;
                            }
                            else{
                                q.enqueue(table,menu,number);
                                s.setValue(menu,s.getValue(menu)-number);
                            }
                        }
                        
                    }
                }

                else if (text == "dequeue"){
                    q.dequeue();
                }

                else if (text == "checkQueue"){
                    int x;
                    cout << "What table do you check : ";
                    cin >> x;
                    if(t.getValue(x-1) == 0){
                        cout << "This table isnt booked yet" << endl;
                    }
                    else{
                        q.checkQueue(x);
                    }
                }

                else if(text ==  "display"){
                    q.display();
                }
                else if(text == "menu"){
                    break;
                }
            }
        }

        if (mode == "exit"){
            cout << "See you again next time"<<endl;
            break;
        }

    }

    return 0;
}
