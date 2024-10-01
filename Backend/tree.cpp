#include <iostream>
#include <queue> // Use <queue> instead of <bits/stdc++.h> for better practice
using namespace std;

class Node {
public:
    int data;
    Node* left;
    Node* right;

    Node(int value) {
        data = value;
        left = NULL;
        right = NULL;
    }
};

class BTree {
protected:
    Node* root;
    void inorder(Node*ptr){
        if(ptr==NULL) return;
        inorder(ptr->left);
        cout<< ptr->data<< " ";
        inorder(ptr->right);
    }
    void preorder(Node*ptr){
        if(ptr==NULL) return;
        cout<< ptr->data<< " ";
        preorder(ptr->left);
        preorder(ptr->right);
    }
    void postorder(Node*ptr){
        if(ptr==NULL) return;
        postorder(ptr->left);
        postorder(ptr->right);
        cout<< ptr->data<< " ";
    }

public:
    BTree() {
        root = NULL;
    }

    void insert(int value) {
        if (root == NULL) {
            root = new Node(value);
            return;
        }

        queue<Node*> q;
        q.push(root);

        while (!q.empty()) {
            Node* ptr = q.front();
            q.pop();

            // Check the left child
            if (ptr->left == NULL) {
                ptr->left = new Node(value);
                break;
            } else {
                q.push(ptr->left);
            }

            // Check the right child
            if (ptr->right == NULL) {
                ptr->right = new Node(value);
                break;
            } else {
                q.push(ptr->right);
            }
        }
    }

    // Function to print the tree (for testing purposes)
    void levelOrderTraversal() {
        if (root == NULL) return;

        queue<Node*> q;
        q.push(root);

        while (!q.empty()) {
            Node* ptr = q.front();
            q.pop();
            cout << ptr->data << " ";

            if (ptr->left != NULL) {
                q.push(ptr->left);
            }
            if (ptr->right != NULL) {
                q.push(ptr->right);
            }
        }
        cout << endl;

    }
    void show(){
    cout<< "root :"<< root -> data<< endl;
    cout<< "root->left->right->left :"<<root->left->right->left->data<<endl;
    cout<< "root->left->left :"<<root->left->left->data<<endl;
    }
    void inorder(){
    inorder(root);
}
  void preorder(){
    preorder(root);
}
  void postorder(){
    postorder(root);
}
};

class BSTree :public BTree{
  Node* insert(Node* ptr,int value){
      if (ptr == NULL) return new Node(value);
      if (value < ptr->data)
        ptr->left = insert(ptr->left,value);
      if (value > ptr->data)
        ptr->right = insert(ptr->right,value);

      return ptr;

  }

  Node* del(Node* ptr,int value){
    if (ptr == NULL) return ptr;
    if(value < ptr->data){
        ptr->left = del(ptr->left,value);
    }
    else if(value > ptr->data){
        ptr->right = del(ptr->right,value);
    }
    else{
        if(ptr -> left == NULL && ptr -> right == NULL){
            delete (ptr);
            return NULL;
        }
        else if(ptr->left == NULL){
            Node* tmp = ptr;
            ptr = ptr->right;
            delete(tmp);
        }
        else if (ptr -> right == NULL){
            Node* tmp = ptr;
            ptr = ptr->left;
            delete(tmp);
        }
        else{
            Node* maxNode = findMax(ptr->left);
            ptr->data = maxNode->data;
            ptr->left = del(ptr->left,maxNode->data);
        }
    }
    
    return ptr;
  }

  Node* findMin(Node* ptr){
    while(ptr->left != NULL){
        ptr = ptr->left;
    }
    return ptr;
  }

  Node* findMax(Node* ptr){
    while(ptr->right != NULL){
        ptr = ptr->right;
    }
    return ptr;
  }




  public:
      void insert(int value){
        root = insert(root,value);
      }

      void del(int value){
        root = del(root,value);
      }
    
    void printMin(){
        Node* ptr = findMin(root);
        cout << ptr -> data << endl;
    }

    void printMax(){
        Node* ptr = findMax(root);
        cout << ptr -> data << endl;
    }

};


int main() {
    BSTree tree = BSTree();
    tree.insert(10);
    tree.insert(15);
    tree.insert(20);
    tree.insert(99);
    tree.insert(88);
    tree.insert(76);
    tree.insert(65);
    tree.insert(24);
    tree.insert(32);
    tree.insert(50);
    tree.insert(9);
    tree.inorder();
    cout << " =================================" << endl;
    tree.del(24);
    tree.del(32);
    tree.del(15);
    tree.del(50);
    tree.inorder();

    return 0;
}
