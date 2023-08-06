/*
Orisvaldo Salviano Neto

Brute Force Code, inspired by Max Tegmark's original Fortran Brute Force Codes

code1 solves for gradients
code2 solves normal way, no pre factors
code3 solves normal way with pre factors
code4 solves normal way only multiplicative factor
code5 solves normal way only additive factor

Operations:

Binary:
 +: add
 *: multiply
 -: subtract
 /: divide	(Put "D" instead of "/" in file, since f77 can't load backslash

 Unary:
  >: increment (x -> x+1)
  <: decrement (x -> x-1)
  ~: negate  	(x-> -x)
  \: invert    (x->1/x) (Put "I" instead of "\" in file, since f77 can't load backslash
  L: logaritm: (x-> ln(x)
  E: exponentiate (x->exp(x))
  S: sin:      (x->sin(x))
  C: cos:      (x->cos(x))
  A: abs:      (x->abs(x))
  N: arcsin:   (x->arcsin(x))
  T: arctan:   (x->arctan(x))
  R: sqrt	(x->sqrt(x))
  O: x->2x
  J: x->2x+1
  H: Dilogarithm 

 nonary:
  0
  1
  P = pi
  a, b, c, ...: input variables for function (need not be listed in functions.dat)

Oris
Last update: 8/05/2020 6:30

*/

#define PY_SSIZE_T_CLEAN
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <string.h>
#include <fstream>
#include <math.h>
#include <tgmath.h>
#include <cmath>
#include <unistd.h>
#include <cstdlib>
#include <gsl/gsl_sf_dilog.h>
#include <Python.h>
//#include <errcode.h>


using namespace std;

double ra = 1.0E30;
double re = 1.0E-15;
double ep = pow(2, 30);
const int par = 21;
const int bae = 300000; //10000000
double xy[2*par][bae], xy0[2*par][bae]; //10000000
double fun[bae][par];
int radix[bae];
bool done = 0;
int nn[3] = {0, 0, 0};
string espa[50], usstr0[10], usstr[10];
double minim = 1;
double z, lossbits[bae], meanbits, bestbits, bitsum, bitexcess, sigma, ev, funtot, funtot_sq, ytot, prodt, pmnum, pmden, xmax = 0, xmin = 1E10;
double denom;
string mysteryfile, outfile, comline, functions = "+*-/><~ILESCANTROJH01P", ops, formula;  //using I instead of /-mirror
int arities[22] = {2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0}, nvarmax = 20, nmax = bae, lnblnk;
int g[10];
double newloss;
double f; //using epsi instead of epsilon and Dl's instead of DL's
double Dl, Dl2;
int ii[bae],kk[bae], i, j, n,jmax, jmin;
int nformulas, nevals, ndata, nvar;
string func[3];
string templat, usedfuncs;
//double nu = 5.;
double premfac, preafac, t_premfac, t_preafac;
//double bitmargin = 0.;

struct output{
  vector <double> meanbits_fin;
  vector <string> ops_fin;
  vector <int> nformulas_fin;
  vector <double> Dl_fin;
  vector <double> Dl2_fin;
  vector <double> sigma_fin;
  vector <double> ev_fin;
  vector <int> times_fin;
  int number;
};

struct output2{
  vector <double> meanbits_fin;
  vector <string> ops_fin;
  vector <int> nformulas_fin;
  vector <double> sigma_fin;
  vector <double> ev_fin;
  vector <double> Dl_fin;
  vector <int> times_fin;
  int number;
};

struct output3{
  vector <double> meanbits_fin;
  vector <double> premfac_fin;
  vector <string> ops_fin;
  vector <double> preafac_fin;
  vector <int> nformulas_fin;
  vector <double> sigma_fin;
  vector <double> ev_fin;
  vector <double> Dl_fin;
  vector <int> times_fin;
  int number;
};

struct output_uno{
  vector <double> prefac_fin;
  vector <string> ops_fin;
  int number;
};

void multiloop(int n, int bases[], int i[]){ //what does this do?
    int k;
    done = 0;
    k=0;
    while(k<=n and !done){
    i[k]++;
    if(i[k]<bases[k]){
      return;
    }
    i[k]=0;
    k++;
    }
    done = 1;
    return;
}

void LoadMatrixTranspose(string f){ //it loads the data table into the code (as the transpost matrix)
    ifstream fil5;
    fil5.open(f);
    if(fil5.fail()){
      cerr<<"DEATH ERROR: Oppening the data file"<<endl;
      exit(1);
    }
    int h=0;
    int d=0;
    while(!(fil5.peek() == '\n')){
        fil5 >> xy0[h][d];
        h++;
    }
    for(int z=1; !fil5.eof(); z++){
        d++;
        for(int l=0;l < h; l++){
            fil5 >> xy0[l][z];
        }
    }
    fil5.close();
    cout<<(d)<<" rows and "<<h<<" columns read from file "<<f<<endl;
    ndata = d;
    nvar = h-1;
    int listind[ndata];
    for(int z=0;z<ndata;z++){
      listind[z]=z;
    }
    std::random_shuffle(listind, listind + ndata);
    for(int z=0;z<ndata;z++){
      for(int zz=0;zz< nvar + 1;zz++){
        xy[zz][z] = xy0[zz][listind[z]];
      }
    }
    //auto end = chrono::steady_clock::now();
    //time[2]+=chrono::duration_cast<chrono::milliseconds>(end - start).count();

    return;
}

double fu(int q,int n, int arities[], string ops, double x[][bae]){
  int nmax, je, arity;
  nmax = 100;
  double y, stack[nmax];
  char op;
  je=-1;
  for(int g=0; g<n; g++){
      arity = arities[g];
      op = ops[g];
      if(arity == 0){ //0-nary
          if(op == '0'){
              y = 0;
          }else if(op == '1'){
              y = 1;
          }else if(op == 'P'){
              y = 4*(atan(1));
          }else{
              y = (xy[op-'a'][q]);
          }
      }else if(arity == 1){ //1-nary
          if(op == '>'){
              y = stack[je] + 1;
          }else if(op == '<'){
              y = stack[je] - 1;
          }else if(op == '~'){
              y = 0 - stack[je];
          }else if(op == 'I'){
              y = (1/stack[je]);
          }else if(op == 'L'){
              y = log(stack[je]);
          }else if(op == 'E'){
              y = exp(stack[je]);
          }else if(op == 'S'){
              y = sin(stack[je]);
          }else if(op == 'C'){
              y = cos(stack[je]);
          }else if(op == 'A'){
              y = abs(stack[je]);
          }else if(op == 'N'){
              y = asin(stack[je]);
          }else if(op == 'T'){
              y = atan(stack[je]);
          }else if (op == 'R'){
              y = sqrt(stack[je]);
          }else if(op == 'O'){
              y = (2*stack[je]);
          }else if(op == 'H'){
              y = gsl_sf_dilog(stack[je]);
          }else{
              y = (2*stack[je] + 1);
          }
      }else{ // 2-nary
          if(op == '+'){
              y = stack[je-1] + stack[je];
          }else if(op == '-'){
              y = stack[je-1] - stack[je];
          }else if(op == '*'){
              y = stack[je-1]*stack[je];
          }else{
              y = (stack[je-1]/stack[je]);
          }
      }
      je = je + 1 -arity;
      stack[je] = y;
  }
  if(je != 0){
      cout<<"DEATH ERROR: STACK UNBALANCED"<<endl;
      exit(1);
  }
  return stack[0];
}

string nume(double a, int g){
  int po = log(abs(a))/log(10);
  double un = pow(10, ((log(abs(a))/log(10)) - po));
  string fin ="";
  if(a<0){
    fin += "-";
  }else if(g==1){
    fin += " ";
  }
  if(po > -200){
    if(po == 0){
      fin += " " + to_string(un);
    }else if(po == 1){
      fin += to_string(10*un);
    }else{
      fin += " " + to_string(un);
      fin+="e" + to_string(po);
    }
  }else{
    fin += " 0.000000";
  }
  return fin;
}

double grad(int q,int n, int arities[], string ops, int f){
  double led[2];
  xy[f][q] += ep;
  led[1] = fu(q, n, arities, ops, xy);
  xy[f][q] -= 2*ep;
  led[0] = fu(q, n, arities, ops, xy);
  xy[f][q] += ep;
  return ((led[1]-led[0])/(2*ep));
}

double bitloss(int nvar, int f){
  double dot, loss;
  dot = 0;
  for(int h = nvar; h < 2*nvar; h++){
    dot += xy[h][f]*fun[f][h - nvar];
  }
  loss = (1 - abs(dot))*1073741824;
  if(std::isnan(loss)){
    loss = 1.0E30;
  }
  if(loss > 1){
    return log(abs(loss))/log(2.0);
  }else{
    return 0.0;
  }
}

double prfa(int j, string a){
  double pfa;
  if(a == "*"){
    pfa = (((funtot*ytot) - ((j+1)*prodt))/((funtot*funtot) - ((j+1)*(funtot_sq))));
    if(!(std::isnan(pfa))){
      return pfa;
    }else{
      return t_premfac;
    }
  }else if(a == "+"){
    pfa = (((prodt*funtot) - (funtot_sq*ytot))/((funtot*funtot) - ((j+1)*(funtot_sq))));
    if(!(std::isnan(pfa))){
      return pfa;
    }else{
      return t_preafac;
    }
  }
}

double bitlossng(int nvar, int f, double fun){
  double loss;
  loss = (abs(fun - xy[nvar][f]))*ep;  //
  if(std::isnan(loss)){
    loss = 1.0E30;
  }
  loss = log(loss)/log(2.0) - 10.0;
  if(loss > 0){
    return loss;
  }else{
    return 0.0;
  }
}

string backslashing(string a){
  string b = a;
  std::replace(b.begin(), b.end(), 'I', '\\');
  return b;
}

PyObject* pyfying1(output Mitchell){
    int height = Mitchell.number;
    //PyObject* meanbits_py = PyList_New(0);
    PyObject* ops_py = PyList_New(0);
    //PyObject* nformulas_py = PyList_New(0);
    //PyObject* Dl_py = PyList_New(0);
    //PyObject* Dl2_py = PyList_New(0);
    //PyObject* sigma_py = PyList_New(0);
    //PyObject* ev_py = PyList_New(0);
    //PyObject* times_py = PyList_New(0);
    //PyObject* result = PyList_New(0);

    for(int i = 0; i < height; i++){
      //PyList_Append(meanbits_py, PyFloat_FromDouble(Mitchell.meanbits_fin[i]));
      const char *c = backslashing(Mitchell.ops_fin[i]).c_str();
      PyList_Append(ops_py, PyBytes_FromFormat(c));
      //PyList_Append(nformulas_py, PyLong_FromLong(Mitchell.nformulas_fin[i]));
      //PyList_Append(Dl_py, PyFloat_FromDouble(Mitchell.Dl_fin[i]));
      //PyList_Append(Dl2_py, PyFloat_FromDouble(Mitchell.Dl2_fin[i]));
      //PyList_Append(sigma_py, PyFloat_FromDouble(Mitchell.sigma_fin[i]));
      //PyList_Append(ev_py, PyFloat_FromDouble(Mitchell.ev_fin[i]));
      //PyList_Append(times_py, PyLong_FromLong(Mitchell.times_fin[i]));
    }

    //PyList_Append(result, (ops_py));
    //PyList_Append(result, (meanbits_py));
    //PyList_Append(result, (nformulas_py));
    //PyList_Append(result, (Dl_py));
    //PyList_Append(result, (Dl2_py));
    //PyList_Append(result, (sigma_py));
    //PyList_Append(result, (ev_py));
    //PyList_Append(result, (times_py));
    return ops_py;
}

PyObject* pyfying2(output2 Mitchell){
    int height = Mitchell.number;
    //PyObject* meanbits_py = PyList_New(0);
    PyObject* ops_py = PyList_New(0);
    //PyObject* nformulas_py = PyList_New(0);
    //PyObject* Dl_py = PyList_New(0);
    //PyObject* sigma_py = PyList_New(0);
    //PyObject* ev_py = PyList_New(0);
    //PyObject* times_py = PyList_New(0);
    //PyObject* result = PyList_New(0);

    for(int i = 0; i < height; i++){
      //PyList_Append(meanbits_py, PyFloat_FromDouble(Mitchell.meanbits_fin[i]));
      const char *c = backslashing(Mitchell.ops_fin[i]).c_str();
      PyList_Append(ops_py, PyBytes_FromFormat(c));
      //PyList_Append(nformulas_py, PyLong_FromLong(Mitchell.nformulas_fin[i]));
      //PyList_Append(Dl_py, PyFloat_FromDouble(Mitchell.Dl_fin[i]));
      //PyList_Append(sigma_py, PyFloat_FromDouble(Mitchell.sigma_fin[i]));
      //PyList_Append(ev_py, PyFloat_FromDouble(Mitchell.ev_fin[i]));
      //PyList_Append(times_py, PyLong_FromLong(Mitchell.times_fin[i]));
    }

    //PyList_Append(result, (ops_py));
    //PyList_Append(result, (meanbits_py));
    //PyList_Append(result, (nformulas_py));
    //PyList_Append(result, (Dl_py));
    //PyList_Append(result, (sigma_py));
    //PyList_Append(result, (ev_py));
    //PyList_Append(result, (times_py));
    return ops_py;
}

PyObject* pyfying3(output3 Mitchell){
    int height = Mitchell.number;
    //PyObject* meanbits_py = PyList_New(0);
    PyObject* premfac_py = PyList_New(0);
    PyObject* ops_py = PyList_New(0);
    PyObject* preafac_py = PyList_New(0);
    //PyObject* nformulas_py = PyList_New(0);
    //PyObject* sigma_py = PyList_New(0);
    //PyObject* ev_py = PyList_New(0);
    //PyObject* Dl_py = PyList_New(0);
    //PyObject* times_py = PyList_New(0);
    PyObject* result = PyList_New(0);

    for(int i = 0; i < height; i++){
      //PyList_Append(meanbits_py, PyFloat_FromDouble(Mitchell.meanbits_fin[i]));
      PyList_Append(premfac_py, PyFloat_FromDouble(Mitchell.premfac_fin[i]));
      const char *c = backslashing(Mitchell.ops_fin[i]).c_str();
      PyList_Append(ops_py, PyBytes_FromFormat(c));
      PyList_Append(preafac_py, PyFloat_FromDouble(Mitchell.preafac_fin[i]));
      //PyList_Append(nformulas_py, PyLong_FromLong(Mitchell.nformulas_fin[i]));
      //PyList_Append(sigma_py, PyFloat_FromDouble(Mitchell.sigma_fin[i]));
      //PyList_Append(ev_py, PyFloat_FromDouble(Mitchell.ev_fin[i]));
      //PyList_Append(Dl_py, PyFloat_FromDouble(Mitchell.Dl_fin[i]));
      //PyList_Append(times_py, PyLong_FromLong(Mitchell.times_fin[i]));
    }

    PyList_Append(result, (premfac_py));
    PyList_Append(result, (ops_py));
    PyList_Append(result, (preafac_py));
    //PyList_Append(result, (meanbits_py));
    //PyList_Append(result, (nformulas_py));
    //PyList_Append(result, (sigma_py));
    //PyList_Append(result, (ev_py));
    //PyList_Append(result, (Dl_py));
    //PyList_Append(result, (times_py));
    return result;
}

PyObject* pyfying4(output_uno Mitchell){
    int height = Mitchell.number;
    //PyObject* meanbits_py = PyList_New(0);
    PyObject* prefac_py = PyList_New(0);
    PyObject* ops_py = PyList_New(0);
    PyObject* result = PyList_New(0);

    for(int i = 0; i < height; i++){
      //PyList_Append(meanbits_py, PyFloat_FromDouble(Mitchell.meanbits_fin[i]));
      PyList_Append(prefac_py, PyFloat_FromDouble(Mitchell.prefac_fin[i]));
      const char *c = backslashing(Mitchell.ops_fin[i]).c_str();
      PyList_Append(ops_py, PyBytes_FromFormat(c));
    }

    PyList_Append(result, (prefac_py));
    PyList_Append(result, (ops_py));
    return result;
}

double unpy_double(PyObject* a){
    return PyFloat_AsDouble(a);
}

int unpy_int(PyObject* a){
  return PyLong_AsLong(a);
}

string unpy_string(PyObject* a, int s){ //FIIIIIX
  string c = "";
  int h;
  for(int la = 0; la < s; la ++){
    h = unpy_int(PySequence_Fast_GET_ITEM(a, la)); // PySequence_Fast_GET_ITEM(a, la)
    c += (char)h;
  }
  return c;
}

output gradiv(string opsfile, string arityfile, int nu, double bitmargin, int times, string mysteryfile){  //inputs: xy0, opsfile, nu, bitmargin, ndata, nvar, times so basically a (double xy0[][], string usedfuncs, double nu, double bitmargin, int ndata, int nvar, int times)
  for(int j = 0; j < 3; j++){
    nn[j] = 0;
    func[j] = "";
  }
  output Mitchell;
  espa[0]="";
  for(int j=1;j<50;j++){
    espa[j] = espa[j-1];
    espa[j] += " ";
  }
  ifstream fil2;
  //cout<<"Number of examples......"<<ndata<<endl;
  cout<<"Loading mystery data...."<<endl;
  LoadMatrixTranspose(mysteryfile);
  cout<<"Number of examples......"<<ndata<<endl;
  if(nvar > nvarmax){
      cout<<"DEATH ERROR: TOO MANY VARIABLES";
      exit(1);
  }else{
      cout<<"Number of variables....."<<nvar<<endl;
  }
  fil2.open(opsfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening opsfile" << opsfile <<endl;
      exit(1);
  }
  usedfuncs = "";
  fil2 >> usedfuncs;
  fil2.close();
  for(int f=0; f < usedfuncs.size();f++){
      if(usedfuncs[f] == 'D'){
        usedfuncs[f] = '/';
      }
      j = functions.find(usedfuncs[f]);
      if((j == 0) and (functions[0] != usedfuncs[f])){
        cout<<"DEATH ERROR: Unknown function requested: "<<usedfuncs[f]<<endl;
        exit(1);
      }else if((j != 0) or (functions[0] == usedfuncs[f])){
        func[arities[j]]+=functions[j];
        nn[arities[j]]++;
      }
  }
  cout<<"Functions used.........."<<usedfuncs<<endl; //check with line 96
  for(int f=0;f < 3;f++){
    cout<<"Arity "<<f<<": ";
    for(int t=0;t<(nn[f]+1);t++){
      cout<<func[f][t]<<" ";
    }
    cout<<endl;
  }
  for(int f=0;f<nvar;f++){
      nn[0]++;
      func[0]+=(97+f);
  }
  for(int i=0;i<ndata;i++){
      denom=0;
      for(int f=nvar; f<(2*nvar); f++){
        denom+=pow(xy0[f][i], 2);
      }
      denom = sqrt(denom);
      for(int f=nvar; f<(2*nvar); f++){
        xy0[f][i] = (xy0[f][i]/max(denom, 1.0E-30));
      }
  }
  cout << "Searching for best fit for matching gradients' directions..."<<endl;
  usstr0[0] = "Meanbits              ";
  usstr0[1] = "equation              ";
  usstr0[2] = "equation's#           ";
  usstr0[3] = "dl                    ";
  usstr0[4] = "dl2                   ";
  usstr0[5] = "";
  usstr0[6] = "";
  usstr0[7] = "sigma                 ";
  usstr0[8] = "ev                    ";
  usstr0[9] = "time";
  for(int i=0;i<10;i++){
    cout << usstr0[i];
  }
  cout << endl;
  nformulas = 0;
  nevals = 0;
  bestbits = 1.e6;
  sigma = 1.e40;
  templat = "";
  fil2.open(arityfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening " << arityfile << endl;
      exit(1);
    }
  time_t endw;
  time_t start;
  start = time(NULL);
  endw = time(NULL) + times;
  while(!fil2.eof() and (time(NULL) < endw)){
      fil2 >> templat;
      n = templat.size();
      for(int f=0;f<n;f++){
        ii[f] = templat[f]-48;
        radix[f]=nn[ii[f]];
        kk[f]=0;
      }
      done = 0;
      while((bestbits>0) and !(done)){

        ops="";
        nformulas++;
        for(int f=0; f<n; f++){
          ops+=func[ii[f]][kk[f]];
        }
        j = 0;
        bitsum = 0;
        z = 0;
        while((z < nu) and (j < ndata)){
          nevals ++;
          denom=0;
          for(int f=0;f<nvar;f++){
            fun[j][f] = grad(j, n, ii, ops, f);
            denom += pow(fun[j][f], 2);
          }
          denom = sqrt(denom);
          for(int f=0;f<nvar;f++){
            fun[j][f] = (fun[j][f]/max(denom, 1.0E-30));
          }

          lossbits[j] = bitloss(nvar, j);
          bitsum += lossbits[j];
          meanbits = (1.0*bitsum/(j+1));
          bitexcess = (meanbits - bestbits - bitmargin);
          z = sqrt(j+1)*(bitexcess/sigma);
          j++;
        }
        if(bitexcess < 0){ //yay new fit!!
          bestbits = min(meanbits,bestbits);
          sigma = 0.0;
          for(int f=0; f<ndata;f++){
            sigma += pow((lossbits[j]-meanbits),2);  //shoudnt've be += ?? it's just = at the fortran code
          }
          sigma = sqrt((sigma/ndata));
          Dl  = 1.44269504089*log(nformulas);
          ev = (1.0*nevals)/nformulas;
          g[0] = (usstr0[0].size() - nume(meanbits,1).size());
          g[1] = (usstr0[1].size() - ops.size());
          g[2] = (usstr0[2].size() - to_string(nformulas).size());
          g[3] = (usstr0[3].size() - nume(Dl,1).size());
          g[4] = (usstr0[4].size() - nume((Dl + ndata*meanbits),1).size());
          //g[5] = (usstr0[5].size() - nume(rmsloss,1).size());
          //g[6] = (usstr0[6].size() - nume(maxloss,1).size());
          g[7] = (usstr0[7].size() - nume(sigma,1).size());
          g[8] = (usstr0[8].size() - nume(ev,1).size());
          usstr[0] = nume(meanbits,1) + espa[abs(g[0])];
          usstr[1] = ops + espa[abs(g[1])];
          usstr[2] = to_string(nformulas) + espa[abs(g[2])];
          usstr[3] = nume(Dl,1) + espa[abs(g[3])];
          usstr[4] = nume((Dl + ndata*meanbits),1) + espa[abs(g[4])];
          usstr[5] = "";
          usstr[6] = "";
          usstr[7] = nume(sigma,1) + espa[abs(g[7])];
          usstr[8] = nume(ev,1) + espa[abs(g[8])];
          usstr[9] = to_string(time(NULL) - start) + "s";
          for(int f=0; f<10; f++){
            cout << usstr[f];
          }
          cout<<endl;
          Mitchell.ops_fin.push_back(ops);
        }
        multiloop(n, radix, kk);
      }
    }
  fil2.close();
  Mitchell.number = Mitchell.ops_fin.size(); //Mitchell.number = gredo;
  return Mitchell;
}

output2 brufo(string opsfile, string arityfile, int nu, double bitmargin, int times, string mysteryfile){
  for(int j = 0; j < 3; j++){
    nn[j] = 0;
    func[j] = "";
  }
  output2 Mitchell;
  espa[0]="";
  for(int j=1;j<50;j++){
    espa[j] = espa[j-1];
    espa[j] += " ";
  }
  cout<<"Loading mystery data...."<<endl;
  LoadMatrixTranspose(mysteryfile);
  ifstream fil2;
  double fun[ndata];
  cout<<"Number of examples......"<<ndata<<endl;
  if(nvar > nvarmax){
    cout<<"DEATH ERROR: TOO MANY VARIABLES";
    exit(1);
  }else{
    //fuse();
    cout<<"Number of variables....."<<nvar<<endl;
  }
  fil2.open(opsfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening opsfile" << opsfile <<endl;
      exit(1);
  }
  usedfuncs = "";
  fil2 >> usedfuncs;
  fil2.close();
  for(int f=0; f < usedfuncs.size();f++){
    if(usedfuncs[f] == 'D'){
      usedfuncs[f] = '/';
    }
    j = functions.find(usedfuncs[f]);
    if((j == 0) and (functions[0] != usedfuncs[f])){
      cout<<"DEATH ERROR: Unknown function requested: "<<usedfuncs[f]<<endl;
      exit(1);
    }else if((j != 0) or (functions[0] == usedfuncs[f])){
      func[arities[j]]+=functions[j];
      nn[arities[j]]++;
    }
  }
  for(int f=0;f<nvar;f++){
    nn[0]++;
    func[0]+=(97+f);
  }
  cout<<"Functions used.........."<<usedfuncs<<endl; //check with line 96
  for(int f=0;f < 3;f++){
    cout<<"Arity "<<f<<": ";
    for(int t=0;t<(nn[f]+1);t++){
      cout<<func[f][t]<<" ";
    }
    cout<<endl;
  }
  nformulas = 0;
  templat = " ";
  fil2.open(arityfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening " << arityfile <<endl;
      exit(1);
  }
  ofstream fil3;
  cout << "Searching for best fit........"<<endl;
  usstr0[0] = "meanbits             ";
  usstr0[1] = ""; //"k1                   ";
  usstr0[2] = "formula              ";
  usstr0[3] = ""; //"k2                   ";
  usstr0[4] = "formula's #          ";
  usstr0[5] = "Sigma                ";
  usstr0[6] = "ev                   ";
  usstr0[7] = "Dl                   ";
  usstr0[8] = ""; //"Newloss              "; //"dl3                  ";
  usstr0[9] = "time";
  for(int i=0;i<10;i++){
    cout << usstr0[i];
  }
  cout << endl;
  double minlc = 0;
  time_t endw;
  time_t start;
  start = time(NULL);
  endw = time(NULL) + times;
  nevals = 0;
	bestbits = 1.e6;
  sigma = 1.e40;
  templat = "";
  while(!fil2.eof() and (time(NULL) < endw)){
    fil2 >> templat;
    n = templat.size();
    for(int f=0;f<n;f++){
      ii[f] = templat[f]-48;
      radix[f]=nn[ii[f]];
      kk[f]=0;
    }
    done = 0;
    while(bestbits>0 and !(done)){
      ops="";
      nformulas++;
      for(int f=0; f<n; f++){
        ops+=func[ii[f]][kk[f]];
      }
      j = 0;
      bitsum = 0;
      z = 0;
      while((z < nu) and (j < ndata)){
        nevals ++;
        fun[j] = fu(j, n, ii, ops, xy);
        lossbits[j] = bitlossng(nvar, j, fun[j]);
        bitsum += lossbits[j];
        meanbits = (1.0*bitsum/(j+1));
        bitexcess = (meanbits - bestbits - bitmargin);
        z = sqrt(j+1)*(bitexcess/sigma);
        j++;
      }
      if((bitexcess < 0)){ //yay new fit!!                 or ops == ""
        bestbits = min(meanbits,bestbits);
        sigma = 0.0;
        for(int f=0; f<ndata;f++){
          sigma += pow((lossbits[f] - meanbits) , 2); //devo colocar esse xy[nvar+1] ou so nvar?
        }
        sigma = sqrt(sigma/ndata);
        Dl  = 1.44269504089*log(nformulas);
        ev = (1.0*nevals)/nformulas;
        g[0] = (usstr0[0].size() - nume(meanbits,1).size());
        //g[1] = (usstr0[1].size() - nume(premfac,1).size());                      //                    .size() - ops.size());
        g[2] = (usstr0[2].size() - ops.size()); //    to_string(nformulas).size());
        //g[3] = (usstr0[3].size() - nume(preafac,1).size());
        g[4] = (usstr0[4].size() - to_string(nformulas).size());
        g[5] = (usstr0[5].size() - nume(sigma,1).size());
        g[6] = (usstr0[6].size() - nume(ev,1).size());
        g[7] = (usstr0[7].size() - nume(Dl,1).size());
        //g[8] = (usstr0[8].size() - nume(newloss,1).size());
        usstr[0] = nume(meanbits,1) + espa[abs(g[0])];
        usstr[1] = ""; //nume(premfac,1) + espa[abs(g[1])];
        usstr[2] = ops + espa[abs(g[2])];
        usstr[3] = ""; //nume(preafac,1) + espa[abs(g[3])];
        usstr[4] = to_string(nformulas) + espa[abs(g[4])];
        usstr[5] = nume(sigma,1) + espa[abs(g[5])];
        usstr[6] = nume(ev,1) + espa[abs(g[6])];
        usstr[7] = nume(Dl,1) + espa[abs(g[7])];
        usstr[8] = ""; //nume(newloss,1) + espa[abs(g[8])];
        usstr[9] = to_string(time(NULL) - start) + "s";
        for(int f=0; f<10; f++){
          cout << usstr[f];
        }
        cout << endl;
        Mitchell.meanbits_fin.push_back(meanbits);
        Mitchell.ops_fin.push_back(ops);
        Mitchell.nformulas_fin.push_back(nformulas);
        Mitchell.sigma_fin.push_back(sigma);
        Mitchell.ev_fin.push_back(ev);
        Mitchell.Dl_fin.push_back(Dl);
        Mitchell.times_fin.push_back(time(NULL) - start);
      }
      multiloop(n, radix, kk);
    }
  }
  fil2.close();
  int gredo = Mitchell.meanbits_fin.size();
  if((Mitchell.meanbits_fin.size() != gredo) or (Mitchell.ops_fin.size() != gredo) or (Mitchell.nformulas_fin.size() != gredo) or (Mitchell.Dl_fin.size() != gredo) or (Mitchell.sigma_fin.size() != gredo) or (Mitchell.ev_fin.size() != gredo) or (Mitchell.times_fin.size() != gredo)){
    cerr << "DEATH ERROR: Number of Pareto Frontiers parameters isn't consistent\n";
    exit(1);
  }
  Mitchell.number = gredo;
  return Mitchell;
}

output3 aamcbrufo(string opsfile, string arityfile, int nu, double bitmargin, int times, string mysteryfile){
  for(int j = 0; j < 3; j++){
    nn[j] = 0;
    func[j] = "";
  }
  preafac = 0;
  premfac = 1;
  t_preafac = 0;
  t_premfac = 1;
  output3 Mitchell;
  espa[0]="";
  for(int j=1;j<50;j++){
    espa[j] = espa[j-1];
    espa[j] += " ";
  }
  ifstream fil2;
  cout<<"Loading mystery data...."<<endl;
  LoadMatrixTranspose(mysteryfile);
  for(int f=0;f<ndata;f++){
    if(abs(xy[nvar][f]) > xmax){
      xmax = xy[nvar][f];
      jmax = f;
    }
    if(abs(xy[nvar][f]) < xmin){
      xmin = xy[nvar][f];
      jmin = f;
    }
  }
  double fun[ndata];
  cout<<"Number of examples......"<<ndata<<endl;
  if(nvar > nvarmax){
    cout<<"DEATH ERROR: TOO MANY VARIABLES";
    exit(1);
  }else{
    //fuse();
    cout<<"Number of variables....."<<nvar<<endl;
  }
  fil2.open(opsfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening opsfile" << opsfile <<endl;
      exit(1);
  }
  usedfuncs = "";
  fil2 >> usedfuncs;
  fil2.close();
  for(int f=0; f < usedfuncs.size();f++){
    if(usedfuncs[f] == 'D'){
      usedfuncs[f] = '/';
    }
    j = functions.find(usedfuncs[f]);
    if((j == 0) and (functions[0] != usedfuncs[f])){
      cout<<"DEATH ERROR: Unknown function requested: "<<usedfuncs[f]<<endl;
      exit(1);
    }else if((j != 0) or (functions[0] == usedfuncs[f])){
      func[arities[j]]+=functions[j];
      nn[arities[j]]++;
    }
  }
  for(int f=0;f<nvar;f++){
    nn[0]++;
    func[0]+=(97+f);
  }
  cout<<"Functions used.........."<<usedfuncs<<endl; //check with line 96
  for(int f=0;f < 3;f++){
    cout<<"Arity "<<f<<": ";
    for(int t=0;t<(nn[f]+1);t++){
      cout<<func[f][t]<<" ";
    }
    cout<<endl;
  }
  nformulas = 0;
  templat = " ";
  fil2.open(arityfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening " << arityfile <<endl;
      exit(1);
  }
  ofstream fil3;
  cout << "Searching for best fit for k1, k2 and formula (equation: k1*(formula) + k2)..."<<endl;
  usstr0[0] = "meanbits             ";
  usstr0[1] = "k1                   ";
  usstr0[2] = "formula              ";
  usstr0[3] = "k2                   ";
  usstr0[4] = "formula's #          ";
  usstr0[5] = "Sigma                ";
  usstr0[6] = "ev                   ";
  usstr0[7] = "Dl                   ";
  usstr0[8] = ""; //"Newloss              "; //"dl3                  ";
  usstr0[9] = "time";
  for(int i=0;i<10;i++){
    cout << usstr0[i];
  }
  cout << endl;
  double minlc = 0;
  time_t endw;
  time_t start;
  start = time(NULL);
  endw = time(NULL) + times;
  nevals = 0;
	bestbits = 1.e6;
  sigma = 1.e40;
  templat = "";
  while(!fil2.eof() and (time(NULL) < endw)){
    fil2 >> templat;
    n = templat.size();
    for(int f=0;f<n;f++){
      ii[f] = templat[f]-48;
      radix[f]=nn[ii[f]];
      kk[f]=0;
    }
    done = 0;
    while(bestbits > 0 and !(done)){
      ops="";
      nformulas++;
      for(int f=0; f<n; f++){
        ops+=func[ii[f]][kk[f]];
      }
      j = 0;
      bitsum = 0;
      z = 0;
      newloss = 0.;
      funtot = 0.;
      ytot = 0.;
      //funtot_sq = 0.;
      //prodt = 0.;
      pmnum = 0.;
      pmden = 0.;
      t_premfac = ((xy[nvar][jmax] - xy[nvar][jmin])/(fu(jmax, n, ii, ops, xy) - fu(jmin, n, ii, ops, xy)));
      if(std::isnan(t_premfac)){
        t_premfac = 1;
      }
      t_preafac = (xy[nvar][jmin] - (t_premfac*(fu(jmin, n, ii, ops, xy))));
      if(std::isnan(t_preafac)){
        t_preafac = 0;
      }
      while((z < nu) and (j < ndata)){
        nevals ++;
        fun[j] = fu(j, n, ii, ops, xy);
        ytot += xy[nvar][j];
        funtot += fun[j];
        //funtot_sq += (fun[i]*fun[i]);
        //prodt += fun[j]*xy[nvar][j];

        pmnum += fun[j]*(xy[nvar][j] - (ytot/(j+1)));
        pmden += fun[j]*(fun[j] - (funtot/(j+1)));
        premfac = pmnum/pmden;
        preafac = (ytot/(j+1)) - premfac*(funtot/(j+1));
        if(std::isnan(premfac)){
          premfac = t_premfac;
        }
        if(std::isnan(preafac)){
          preafac = t_preafac;
        }

        //premfac = prfa(j, "*");
        //preafac = prfa(j, "+");
        //lossbits[j] = bitlossng(nvar, j, (((((ndata-j)/ndata)*t_premfac) + ((j/ndata)*premfac))*fun[j] + ((((ndata-j)/ndata)*t_preafac) + ((j/ndata)*preafac))));
        lossbits[j] = bitlossng(nvar, j, (premfac*fun[j] + preafac));
        bitsum += lossbits[j];
        meanbits = (1.0*bitsum/(j+1));
        bitexcess = (meanbits - bestbits - bitmargin);
        z = sqrt(j+1)*(bitexcess/sigma);
        j++;
      }
      if(bitexcess < 0){ //yay new fit!!                 or ops == ""
        bestbits = min(meanbits,bestbits);
        sigma = 0.0;
        for(int f=0; f<ndata;f++){
          newloss += pow((xy[nvar][j] - premfac*fun[j]), 2);
        }
        newloss = sqrt(newloss/ndata);
        for(int f=0; f<ndata;f++){
          sigma += pow((lossbits[f] - meanbits) , 2); //devo colocar esse xy[nvar+1] ou so nvar?
        }
        sigma = sqrt(sigma/ndata);
        Dl  = 1.44269504089*log(nformulas);
        ev = (1.0*nevals)/nformulas;
        g[0] = (usstr0[0].size() - nume(meanbits,1).size());
        g[1] = (usstr0[1].size() - nume(premfac,1).size());                      //                    .size() - ops.size());
        g[2] = (usstr0[2].size() - ops.size()); //    to_string(nformulas).size());
        g[3] = (usstr0[3].size() - nume(preafac,1).size());
        g[4] = (usstr0[4].size() - to_string(nformulas).size());
        g[5] = (usstr0[5].size() - nume(sigma,1).size());
        g[6] = (usstr0[6].size() - nume(ev,1).size());
        g[7] = (usstr0[7].size() - nume(Dl,1).size());
        //g[8] = (usstr0[8].size() - nume(newloss,1).size());
        usstr[0] = nume(meanbits,1) + espa[abs(g[0])];
        usstr[1] = nume(premfac,1) + espa[abs(g[1])];
        usstr[2] = ops + espa[abs(g[2])];
        usstr[3] = nume(preafac,1) + espa[abs(g[3])];
        usstr[4] = to_string(nformulas) + espa[abs(g[4])];
        usstr[5] = nume(sigma,1) + espa[abs(g[5])];
        usstr[6] = nume(ev,1) + espa[abs(g[6])];
        usstr[7] = nume(Dl,1) + espa[abs(g[7])];
        usstr[8] = ""; //nume(newloss,1) + espa[abs(g[8])];
        usstr[9] = to_string(time(NULL) - start) + "s";
        for(int f=0; f<10; f++){
          cout << usstr[f];
        }
        cout << endl;
        Mitchell.meanbits_fin.push_back(meanbits);
        Mitchell.premfac_fin.push_back(premfac);
        Mitchell.ops_fin.push_back(ops);
        Mitchell.preafac_fin.push_back(preafac);
        Mitchell.nformulas_fin.push_back(nformulas);
        Mitchell.sigma_fin.push_back(sigma);
        Mitchell.ev_fin.push_back(ev);
        Mitchell.Dl_fin.push_back(Dl);
        Mitchell.times_fin.push_back(time(NULL) - start);
      }
      multiloop(n, radix, kk);
    }
  }
  fil2.close();
  int gredo = Mitchell.meanbits_fin.size();
  if((Mitchell.meanbits_fin.size() != gredo) or (Mitchell.premfac_fin.size() != gredo) or (Mitchell.ops_fin.size() != gredo) or (Mitchell.preafac_fin.size() != gredo) or (Mitchell.nformulas_fin.size() != gredo) or (Mitchell.Dl_fin.size() != gredo) or (Mitchell.sigma_fin.size() != gredo) or (Mitchell.ev_fin.size() != gredo) or (Mitchell.times_fin.size() != gredo)){
    cerr << "DEATH ERROR: Number of Pareto Frontiers parameters isn't consistent\n";
    exit(1);
  }
  Mitchell.number = gredo;
  return Mitchell;
}

output_uno mubrufo(string opsfile, string arityfile, int nu, double bitmargin, int times, string mysteryfile){
  for(int j = 0; j < 3; j++){
    nn[j] = 0;
    func[j] = "";
  }
  preafac = 0;
  premfac = 1;
  t_preafac = 0;
  t_premfac = 1;
  output_uno Mitchell;
  espa[0]="";
  for(int j=1;j<50;j++){
    espa[j] = espa[j-1];
    espa[j] += " ";
  }
  ifstream fil2;
  cout<<"Loading mystery data...."<<endl;
  LoadMatrixTranspose(mysteryfile);
  for(int f=0;f<ndata;f++){
    if(abs(xy[nvar][f]) > xmax){
      xmax = xy[nvar][f];
      jmax = f;
    }
    if(abs(xy[nvar][f]) < xmin){
      xmin = xy[nvar][f];
      jmin = f;
    }
  }
  double fun[ndata];
  cout<<"Number of examples......"<<ndata<<endl;
  if(nvar > nvarmax){
    cout<<"DEATH ERROR: TOO MANY VARIABLES";
    exit(1);
  }else{
    //fuse();
    cout<<"Number of variables....."<<nvar<<endl;
  }
  fil2.open(opsfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening opsfile" << opsfile <<endl;
      exit(1);
  }
  usedfuncs = "";
  fil2 >> usedfuncs;
  fil2.close();
  for(int f=0; f < usedfuncs.size();f++){
    if(usedfuncs[f] == 'D'){
      usedfuncs[f] = '/';
    }
    j = functions.find(usedfuncs[f]);
    if((j == 0) and (functions[0] != usedfuncs[f])){
      cout<<"DEATH ERROR: Unknown function requested: "<<usedfuncs[f]<<endl;
      exit(1);
    }else if((j != 0) or (functions[0] == usedfuncs[f])){
      func[arities[j]]+=functions[j];
      nn[arities[j]]++;
    }
  }
  for(int f=0;f<nvar;f++){
    nn[0]++;
    func[0]+=(97+f);
  }
  cout<<"Functions used.........."<<usedfuncs<<endl;
  for(int f=0;f < 3;f++){
    cout<<"Arity "<<f<<": ";
    for(int t=0;t<(nn[f]+1);t++){
      cout<<func[f][t]<<" ";
    }
    cout<<endl;
  }
  nformulas = 0;
  cout << "Searching for best fit for k and formula (equation: k*(formula))..."<<endl;
  usstr0[0] = "meanbits             ";
  usstr0[1] = "k                    ";
  usstr0[2] = "formula              ";
  usstr0[3] = "";
  usstr0[4] = "formula's #          ";
  usstr0[5] = "Sigma                ";
  usstr0[6] = "ev                   ";
  usstr0[7] = "Dl                   ";
  usstr0[8] = ""; //"Newloss              "; //"dl3                  ";
  usstr0[9] = "time";
  for(int i=0;i<10;i++){
    cout << usstr0[i];
  }
  cout << endl;
  fil2.open(arityfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening " << arityfile <<endl;
      exit(1);
  }
  ofstream fil3;
  double minlc = 0;
  time_t endw;
  time_t start;
  start = time(NULL);
  endw = time(NULL) + times;
  nevals = 0;
	bestbits = 1.e6;
  sigma = 1.e40;
  templat = "";
  while(!fil2.eof() and (time(NULL) < endw)){
    fil2 >> templat;
    n = templat.size();
    for(int f=0;f<n;f++){
      ii[f] = templat[f]-48;
      radix[f]=nn[ii[f]];
      kk[f]=0;
    }
    done = 0;
    while(bestbits>0 and !(done)){
      ops="";
      nformulas++;
      for(int f=0; f<n; f++){
        ops+=func[ii[f]][kk[f]];
      }
      j = 0;
      bitsum = 0;
      z = 0;
      newloss = 0.;
      funtot = 0.;
      ytot = 0.;
      //funtot_sq = 0.;
      //prodt = 0.;
      pmnum = 0.;
      pmden = 0.;
      t_premfac = ((xy[nvar][jmax] - xy[nvar][jmin])/(fu(jmax, n, ii, ops, xy) - fu(jmin, n, ii, ops, xy)));
      if(std::isnan(t_premfac)){
        t_premfac = 1;
      }
      while((z < nu) and (j < ndata)){
        nevals ++;
        fun[j] = fu(j, n, ii, ops, xy);
        ytot += xy[nvar][j];
        funtot += fun[j];
        //funtot_sq += (fun[i]*fun[i]);
        //prodt += fun[j]*xy[nvar][j];

        //pmnum += fun[j]*(xy[nvar][j] - (ytot/(j+1)));
        //pmden += fun[j]*(fun[j] - (funtot/(j+1)));
        premfac = pmnum/pmden;
        if(std::isnan(premfac)){
          premfac = t_premfac;
        }

        //premfac = prfa(j, "*");
        lossbits[j] = bitlossng(nvar, j, (premfac*fun[j]));
        //lossbits[j] = bitlossng(nvar, j, (( (((ndata-j)/ndata)*t_premfac) + ((j/ndata)*premfac) )*fun[j]));
        bitsum += lossbits[j];
        meanbits = (1.0*bitsum/(j+1));
        bitexcess = (meanbits - bestbits - bitmargin);
        z = sqrt(j+1)*(bitexcess/sigma);
        j++;
      }
      if((bitexcess < 0)){ //yay new fit!!                 or ops == ""
        bestbits = min(meanbits,bestbits);
        sigma = 0.0;
        for(int f=0; f<ndata;f++){
          newloss += pow((xy[nvar][j] - premfac*fun[j]), 2);
        }
        newloss = sqrt(newloss/ndata);
        for(int f=0; f<ndata;f++){
          sigma += pow((lossbits[f] - meanbits) , 2); //devo colocar esse xy[nvar+1] ou so nvar?
        }
        sigma = sqrt(sigma/ndata);
        Dl  = 1.44269504089*log(nformulas);
        ev = (1.0*nevals)/nformulas;
        g[0] = (usstr0[0].size() - nume(meanbits,1).size());
        g[1] = (usstr0[1].size() - nume(premfac,1).size());                      //                    .size() - ops.size());
        g[2] = (usstr0[2].size() - ops.size()); //    to_string(nformulas).size());
        //g[3] = (usstr0[3].size() - nume(preafac,1).size());
        g[4] = (usstr0[4].size() - to_string(nformulas).size());
        g[5] = (usstr0[5].size() - nume(sigma,1).size());
        g[6] = (usstr0[6].size() - nume(ev,1).size());
        g[7] = (usstr0[7].size() - nume(Dl,1).size());
        //g[8] = (usstr0[8].size() - nume(newloss,1).size());
        usstr[0] = nume(meanbits,1) + espa[abs(g[0])];
        usstr[1] = nume(premfac,1) + espa[abs(g[1])];
        usstr[2] = ops + espa[abs(g[2])];
        usstr[3] = "";//nume(preafac,1) + espa[abs(g[3])];
        usstr[4] = to_string(nformulas) + espa[abs(g[4])];
        usstr[5] = nume(sigma,1) + espa[abs(g[5])];
        usstr[6] = nume(ev,1) + espa[abs(g[6])];
        usstr[7] = nume(Dl,1) + espa[abs(g[7])];
        usstr[8] = ""; //nume(newloss,1) + espa[abs(g[8])];
        usstr[9] = to_string(time(NULL) - start) + "s";
        for(int f=0; f<10; f++){
          cout << usstr[f];
        }
        cout << endl;
        Mitchell.prefac_fin.push_back(premfac);
        Mitchell.ops_fin.push_back(ops);
      }
      multiloop(n, radix, kk);
    }
  }
  fil2.close();
  //int gredo = Mitchell.ops_fin.size();
  if(Mitchell.prefac_fin.size() != Mitchell.ops_fin.size()){
    cerr << "DEATH ERROR: Number of Pareto Frontiers parameters isn't consistent\n";
    exit(1);
  }
  Mitchell.number = Mitchell.ops_fin.size();
  return Mitchell;
}

output_uno adbrufo(string opsfile, string arityfile, int nu, double bitmargin, int times, string mysteryfile){
  for(int j = 0; j < 3; j++){
    nn[j] = 0;
    func[j] = "";
  }
  preafac = 0;
  premfac = 1;
  t_preafac = 0;
  t_premfac = 1;
  output_uno Mitchell;
  espa[0]="";
  for(int j=1;j<50;j++){
    espa[j] = espa[j-1];
    espa[j] += " ";
  }
  ifstream fil2;
  cout<<"Loading mystery data...."<<endl;
  LoadMatrixTranspose(mysteryfile);
  for(int f=0;f<ndata;f++){
    if(abs(xy[nvar][f]) < xmin){
      xmin = xy[nvar][f];
      jmin = f;
    }
  }
  double fun[ndata];
  cout<<"Number of examples......"<<ndata<<endl;
  if(nvar > nvarmax){
    cout<<"DEATH ERROR: TOO MANY VARIABLES";
    exit(1);
  }else{
    //fuse();
    cout<<"Number of variables....."<<nvar<<endl;
  }
  fil2.open(opsfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening opsfile" << opsfile <<endl;
      exit(1);
  }
  usedfuncs = "";
  fil2 >> usedfuncs;
  fil2.close();
  for(int f=0; f < usedfuncs.size();f++){
    if(usedfuncs[f] == 'D'){
      usedfuncs[f] = '/';
    }
    j = functions.find(usedfuncs[f]);
    if((j == 0) and (functions[0] != usedfuncs[f])){
      cout<<"DEATH ERROR: Unknown function requested: "<<usedfuncs[f]<<endl;
      exit(1);
    }else if((j != 0) or (functions[0] == usedfuncs[f])){
      func[arities[j]]+=functions[j];
      nn[arities[j]]++;
    }
  }
  for(int f=0;f<nvar;f++){
    nn[0]++;
    func[0]+=(97+f);
  }
  cout<<"Functions used.........."<<usedfuncs<<endl; //check with line 96
  for(int f=0;f < 3;f++){
    cout<<"Arity "<<f<<": ";
    for(int t=0;t<(nn[f]+1);t++){
      cout<<func[f][t]<<" ";
    }
    cout<<endl;
  }
  nformulas = 0;
  cout << "Searching for best fit for k and formula (equation: (formula) + k)..."<<endl;
  usstr0[0] = "meanbits             ";
  usstr0[1] = "formula              ";
  usstr0[2] = "k                    ";
  usstr0[3] = "";
  usstr0[4] = "formula's #          ";
  usstr0[5] = "Sigma                ";
  usstr0[6] = "ev                   ";
  usstr0[7] = "Dl                   ";
  usstr0[8] = ""; //"Newloss              "; //"dl3                  ";
  usstr0[9] = "time";
  for(int i=0;i<10;i++){
    cout << usstr0[i];
  }
  cout << endl;
  fil2.open(arityfile);
  if(fil2.fail()){
      cerr<<"DEATH ERROR oppening " << arityfile <<endl;
      exit(1);
  }
  ofstream fil3;
  double minlc = 0;
  time_t endw;
  time_t start;
  start = time(NULL);
  endw = time(NULL) + times;
  nevals = 0;
	bestbits = 1.e6;
  sigma = 1.e40;
  templat = "";
  while(!fil2.eof() and (time(NULL) < endw)){
    fil2 >> templat;
    n = templat.size();
    for(int f=0;f<n;f++){
      ii[f] = templat[f]-48;
      radix[f]=nn[ii[f]];
      kk[f]=0;
    }
    done = 0;
    while(bestbits > 0 and !(done)){
      ops="";
      nformulas++;
      for(int f=0; f<n; f++){
        ops+=func[ii[f]][kk[f]];
      }
      j = 0;
      bitsum = 0;
      z = 0;
      newloss = 0.;
      funtot = 0.;
      ytot = 0.;
      //funtot_sq = 0.;
      //prodt = 0.;
      t_preafac = (xy[nvar][jmin] - fu(jmin, n, ii, ops, xy));
      if(std::isnan(t_preafac)){
        t_preafac = 0;
      }
      while((z < nu) and (j < ndata)){
        nevals ++;
        fun[j] = fu(j, n, ii, ops, xy);
        ytot += xy[nvar][j];
        funtot += fun[j];
        //funtot_sq += (fun[i]*fun[i]);
        //prodt += fun[j]*xy[nvar][j];


        preafac = (ytot/(j+1)) - (funtot/(j+1));
        if(std::isnan(preafac)){
          preafac = t_preafac;
        }


        //preafac = prfa(j, "+");
        //lossbits[j] = bitlossng(nvar, j, (fun[j] + t_preafac));
        lossbits[j] = bitlossng(nvar, j, (fun[j] + preafac));
        //lossbits[j] = bitlossng(nvar, j, (fun[j] + ((((ndata-j)/ndata)*t_preafac) + ((j/ndata)*preafac)))); //( (((ndata-j)/ndata)*t_preafac) + ((j/ndata)*preafac) )
        bitsum += lossbits[j];
        meanbits = (1.0*bitsum/(j+1));
        bitexcess = (meanbits - bestbits - bitmargin);
        z = sqrt(j+1)*(bitexcess/sigma);
        j++;
      }
      if((bitexcess < 0)){ //yay new fit!!                 or ops == ""
        bestbits = min(meanbits,bestbits);
        sigma = 0.0;
        for(int f=0; f<ndata;f++){
          newloss += pow((xy[nvar][j] - premfac*fun[j]), 2);
        }
        newloss = sqrt(newloss/ndata);
        for(int f=0; f<ndata;f++){
          sigma += pow((lossbits[f] - meanbits) , 2); //devo colocar esse xy[nvar+1] ou so nvar?
        }
        sigma = sqrt(sigma/ndata);
        Dl  = 1.44269504089*log(nformulas);
        ev = (1.0*nevals)/nformulas;
        g[0] = (usstr0[0].size() - nume(meanbits,1).size());
        //g[1] = (usstr0[1].size() - nume(premfac,1).size());                      //                    .size() - ops.size());
        g[2] = (usstr0[2].size() - ops.size()); //    to_string(nformulas).size());
        g[3] = (usstr0[3].size() - nume(preafac,1).size());
        g[4] = (usstr0[4].size() - to_string(nformulas).size());
        g[5] = (usstr0[5].size() - nume(sigma,1).size());
        g[6] = (usstr0[6].size() - nume(ev,1).size());
        g[7] = (usstr0[7].size() - nume(Dl,1).size());
        //g[8] = (usstr0[8].size() - nume(newloss,1).size());
        usstr[0] = nume(meanbits,1) + espa[abs(g[0])];
        usstr[1] = ""; //nume(premfac,1) + espa[abs(g[1])];
        usstr[2] = ops + espa[abs(g[2])];
        usstr[3] = nume(preafac,1) + espa[abs(g[3])];
        usstr[4] = to_string(nformulas) + espa[abs(g[4])];
        usstr[5] = nume(sigma,1) + espa[abs(g[5])];
        usstr[6] = nume(ev,1) + espa[abs(g[6])];
        usstr[7] = nume(Dl,1) + espa[abs(g[7])];
        usstr[8] = ""; //nume(newloss,1) + espa[abs(g[8])];
        usstr[9] = to_string(time(NULL) - start) + "s";
        for(int f=0; f<10; f++){
          cout << usstr[f];
        }
        cout << endl;
        Mitchell.prefac_fin.push_back(preafac);
        Mitchell.ops_fin.push_back(ops);
      }
      multiloop(n, radix, kk);
    }
  }
  fil2.close();
  //int gredo = Mitchell.ops_fin.size();
  if(Mitchell.prefac_fin.size() != Mitchell.ops_fin.size()){
    cerr << "DEATH ERROR: Number of Pareto Frontiers parameters isn't consistent\n";
    exit(1);
  }
  Mitchell.number = Mitchell.ops_fin.size();
  return Mitchell;
}

extern "C"{  //inputs: xy0, opsfile, nu, bitmargin, ndata, nvar, times so basically a (double xy0[][], string usedfuncs, double nu, double bitmargin, int ndata, int nvar, int times)

  PyObject* code1(PyObject* path_py, PyObject* size3, PyObject* mystery_py, PyObject* size2, PyObject* opsfile_py, PyObject* size1, PyObject* nu_py, PyObject* times_py){ //inputs!
    int size1_cpp = unpy_int(size1);
    string opsfile = unpy_string(opsfile_py, size1_cpp);
    double nu = unpy_int(nu_py);
    //double bitmargin = unpy_double(bitmargin_py);
    int times = unpy_int(times_py);
    int size2_cpp = unpy_int(size2);
    int size3_cpp = unpy_int(size3);
    string mysteryfile = unpy_string(path_py, size3_cpp) + unpy_string(mystery_py, size2_cpp);
    return pyfying1(gradiv(usedfuncs, "arity2templates.txt", nu, 0.0, times, mysteryfile));
  }

  PyObject* code2(PyObject* path_py, PyObject* size3, PyObject* mystery_py, PyObject* size2, PyObject* opsfile_py, PyObject* size1, PyObject* nu_py, PyObject* times_py){ //inputs!
    int size1_cpp = unpy_int(size1);
    string opsfile = unpy_string(opsfile_py, size1_cpp);
    double nu = unpy_int(nu_py);
    //double bitmargin = unpy_double(bitmargin_py);
    int times = unpy_int(times_py);
    int size2_cpp = unpy_int(size2);
    int size3_cpp = unpy_int(size3);
    string mysteryfile = unpy_string(path_py, size3_cpp) + unpy_string(mystery_py, size2_cpp);
    return pyfying2(brufo(opsfile, "arity2templates.txt", nu, 0.0, times, mysteryfile));
  }

  PyObject* code3(PyObject* path_py, PyObject* size3, PyObject* mystery_py, PyObject* size2, PyObject* opsfile_py, PyObject* size1, PyObject* nu_py, PyObject* times_py){ //inputs!
    int size1_cpp = unpy_int(size1);
    string opsfile = unpy_string(opsfile_py, size1_cpp);
    double nu = unpy_int(nu_py);
    //double bitmargin = unpy_double(bitmargin_py);
    int times = unpy_int(times_py);
    int size2_cpp = unpy_int(size2);
    int size3_cpp = unpy_int(size3);
    string mysteryfile = unpy_string(path_py, size3_cpp) + unpy_string(mystery_py, size2_cpp);
    return pyfying3(aamcbrufo(opsfile, "arity2templates.txt", nu, 0.0, times, mysteryfile));
  }

  PyObject* code4(PyObject* path_py, PyObject* size3, PyObject* mystery_py, PyObject* size2, PyObject* opsfile_py, PyObject* size1, PyObject* arityfile_py, PyObject* size0, PyObject* nu_py, PyObject* times_py){ //inputs!
    int size0_cpp = unpy_int(size0);
    int size1_cpp = unpy_int(size1);
    string opsfile = unpy_string(opsfile_py, size1_cpp);
    double nu = unpy_int(nu_py);
    //double bitmargin = unpy_double(bitmargin_py);
    int times = unpy_int(times_py);
    int size2_cpp = unpy_int(size2);
    int size3_cpp = unpy_int(size3);
    string mysteryfile = unpy_string(path_py, size3_cpp) + unpy_string(mystery_py, size2_cpp);
    string arityfile = unpy_string(arityfile_py, size0_cpp);
    return pyfying4(mubrufo(opsfile, arityfile, nu, 0.0, times, mysteryfile));
  }

  PyObject* code5(PyObject* path_py, PyObject* size3, PyObject* mystery_py, PyObject* size2, PyObject* opsfile_py, PyObject* size1, PyObject* arityfile_py, PyObject* size0, PyObject* nu_py, PyObject* times_py){ //inputs!
    int size0_cpp = unpy_int(size0);
    int size1_cpp = unpy_int(size1);
    string opsfile = unpy_string(opsfile_py, size1_cpp);
    double nu = unpy_int(nu_py);
    //double bitmargin = unpy_double(bitmargin_py);
    int times = unpy_int(times_py);
    int size2_cpp = unpy_int(size2);
    int size3_cpp = unpy_int(size3);
    string mysteryfile = unpy_string(path_py, size3_cpp) + unpy_string(mystery_py, size2_cpp);
    string arityfile = unpy_string(arityfile_py, size0_cpp);
    return pyfying4(adbrufo(opsfile, arityfile, nu, 0.0, times, mysteryfile));
  }

}

int main(){
  return 0;
}
