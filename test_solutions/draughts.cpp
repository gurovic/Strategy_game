#include "bits/stdc++.h"
#include <random>


//////////////////////////////////////////// defines ////////////////////////////////////////////////////////////////////////////////////////
#define forn(i,n) for(int i=0; i<n; i++)
#define forx(i,a) for(auto &i:a)
#define fornn(i,n) for(int i=1; i<=n; i++)
#define ford(i,n) for(ll i=n-1; i>=0; i--)
#define fordd(i,n) for(long i=n; i>=2; i--)
#define MAX(a,b,c) max(a,max(b,c))
#define MIN(a,b,c) min(a,min(b,c))
#define all(c) (c).begin(),(c).end()
#define rall(c) (c).rbegin(),(c).rend()
#define pb push_back
#define eb emplace_back
#define ff first
#define ss second

//////////////////////////////////////////// functions //////////////////////////////////////////////////////////////////////////////////////
using namespace std;
using ll=long long;
using ull=unsigned long long;
using pii=pair<int, int>;
using pll=pair<long, long>;
using pLL=pair<ll, ll>;
using mll=map<long, long>;

template <typename typC> ull gcd(typC x, typC y) { return x? gcd(y%x, x) : y; }
template <typename typC> ull lcm(typC x, typC y) { return (ull) x*y/gcd(x, y); }
template <typename typC> ull lcm(vector <typC>& a) {
    ull res=1;
    for (auto& x : a) res=lcm(res, x);
    return res;
}

template <typename typC> ll Vsum(vector <typC>& a) {
    ll res=0;
    forx(x, a) res+=x;
    return res;
}
template <typename typA, typename typB> ll max(typA a, typB b) { return (a>b? a : b); }

/////////////////////////////////////////////// operators //////////////////////////////////////////////////////////////////////////////////////
template <typename typC> istream& operator>>(istream& in, vector <typC>& a) {
    for (auto& x : a) in>>x;
    return in;
}
template <typename typC> istream& operator>>(istream& in, vector <pair<typC, typC>>& a) {
    for (auto& x : a) in>>x.ff>>x.ss;
    return in;
}
template <typename typC> istream& operator>>(istream& in, pair <typC, typC>& a) {
    in>>a.ff>>a.ss;
    return in;
}
template <typename typC> ostream& operator<<(ostream& out, pair <typC, typC>& a) {
    out<<a.ff<<' '<<a.ss;
    return out;
}
template <typename typC> ostream& operator<<(ostream& out, vector <typC>& a) {
    for (auto& x : a) out<<x<<" ";
    return out;
}
template <typename typC> ostream& operator<<(ostream& out, vector <vector<typC>>& a) {
    for (auto& x : a) out<<x<<endl;
    return out;
}


////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
const ll maxn=1e6+5, maxm=1e6+5, inf_int=1e9, inf_ll=1e18, mod=998244353;
struct Grid;
struct EatResult;
struct Moves;
struct QueenEatResult;

// g values
// 0 - пустая клетка
// 1 - моя пешка
// 2 - моя дамка
// 3 - чужая пешка
// 4 - чужая дамка

struct Moves {
    vector<pii> moves;
    pii start;

    Moves() { start={0,0}; moves.clear(); }
    Moves(pii s, vector<pii> m) {
        start=s;
        moves=m;
    }

    friend ostream& operator<<(ostream& out, pair<int,int>& a) {
        out<<a.ff+1<<' '<<a.ss+1;
        return out;
    }

    void addStartPoint(int x, int y) {
        start={x,y};
    }
    void addNewPoint(int x, int y) {
        moves.eb(x,y);
    }
    void addNewPoints(vector<pii> &x) {
        forx(i,x) moves.pb(i);
    }
    void print() {
        cout<<moves.size()<<"\n";
        cout<<start.ff+1<<" "<<start.ss+1<<"\n";
        for(auto &i:moves) cout<<i.ff+1<<" "<<i.ss+1<<" ";
        cout<<endl;
    }
    void read() {
        int n; cin>>n;
        if (n==-1) {
            start={-1,-1};
            return;
        }
        moves.assign(n,{});
        cin>>start;
        start.ff--; start.ss--;
        forn(i,n) cin>>moves[i], moves[i].ff--, moves[i].ss--;
    }
};
struct QueenEatResult {
    vector<pii> path;
    pii start;
    int ate_queens=0, count=0;
    bool lose_queen=false;

    void startPos(pii s) {
        start=s;
    }
    void addDraught(int x, int y, int val) {
        if (val==3) {
            path.eb(x,y);
            count++;
        } else if (val==4) {
            path.eb(x,y);
            count++;
            ate_queens++;
        }
    }
    void loseQueen() {
        lose_queen=true;
    }

    QueenEatResult maxResult(QueenEatResult a, QueenEatResult b) {
        if (a.lose_queen) {
            if (b.lose_queen) {
                if (a.ate_queens>b.ate_queens) return a;
                else if (b.ate_queens>a.ate_queens) return b;
                else return a.count>b.count? a:b;
            } else {
                if (a.ate_queens-1>b.ate_queens) return a;
                else return b;
            }
        } else {
            if (b.lose_queen) {
                if (b.ate_queens-1>a.ate_queens) return b;
                else return a;
            } else {
                if (a.ate_queens>b.ate_queens) return a;
                else if (b.ate_queens>a.ate_queens) return b;
                else return a.count>b.count? a:b;
            }
        }
    }
};
struct EatResult {
    bool is_queen=false;
    int count=0;
    vector<pair<int,int>> path;
    pair<int,int> start;

    EatResult() {
        is_queen=false;
        count=0;
        path.clear();
        start={0,0};
    }
    EatResult(QueenEatResult &res) {
        this->path=res.path;
        this->start=res.start;
        this->count=res.count;
        this->is_queen=res.ate_queens>0;
    }
    void startDraught(int x, int y) {
        this->start={x,y};
    }
    void newDraught(int x, int y, int val) {
        if (val==4) {
            is_queen=true;
            path.eb(x, y);
            count++;
        }
        else if (val==3) {
            path.eb(x,y);
            count++;
        }
    }
    EatResult maxResult(EatResult res1, EatResult res2) {
        if (res1.is_queen && res2.is_queen) return (res1.count > res2.count? res1:res2);
        else if (res1.is_queen) return res1;
        else if (res2.is_queen) return res2;
        else return (res1.count > res2.count? res1:res2);
    }

    Moves getMoves() {
        Moves a;
        a.addStartPoint(start.ff, start.ss);
        a.addNewPoints(path);
        return a;
    }
    void print() {
        Moves a=getMoves();
        a.print();
    }
};
struct Grid {
    const int dx[4]={-1, -1, 1, 1};
    const int dy[4]={1, -1, 1, -1};
    const int d=8, m=4;
    int queens_count=0;
    vector<vector<int>> a;

    Grid() {
        a.clear();

        a.pb({0,3,0,3,0,3,0,3});
        a.pb({3,0,3,0,3,0,3,0});
        a.pb({0,3,0,3,0,3,0,3});
        a.pb({0,0,0,0,0,0,0,0});
        a.pb({0,0,0,0,0,0,0,0});
        a.pb({1,0,1,0,1,0,1,0});
        a.pb({0,1,0,1,0,1,0,1});
        a.pb({1,0,1,0,1,0,1,0});
    }

    bool check(int x, int y) {
        return x>=0 && y>=0 && x<d && y<d;
    }
    void printGrid() {
        forn(i,d) {
            forn(j,d) cout<<a[i][j];
            cout<<"\n";
        }
        cout<<endl;
    }

    EatResult eatByNormal(int x, int y, vector<vector<bool>> &used) {
        EatResult res;

        forn(i,4) {
            int tox=x+dx[i], toy=y+dy[i];
            if (check(tox, toy) && !used[tox][toy]) {
                if (a[tox][toy]==3) {
                    if (check(tox+dx[i], toy+dy[i]) && a[tox+dx[i]][toy+dy[i]]==0) {
                        used[tox][toy]=true;
                        EatResult cur=eatByNormal(tox+dx[i], toy+dy[i], used);
                        cur.newDraught(tox+dx[i], toy+dy[i], a[tox][toy]);
                        res=res.maxResult(res, cur);
                    }
                }
                else if (a[tox][toy]==4) {
                    if (check(tox+dx[i], toy+dy[i]) && a[tox+dx[i]][toy+dy[i]]==0) {
                        EatResult cur=eatByNormal(tox+dx[i], toy+dy[i], used);
                        cur.newDraught(tox+dx[i], toy+dy[i], a[tox][toy]);
                        res=res.maxResult(res, cur);
                    }
                }
            }
        }
        res.startDraught(x,y);
        return res;
    }
    QueenEatResult eatByQueen(int x, int y) {
        QueenEatResult res;

        forn(i,4) {
            int tox=x, toy=y;
            while (true) {
                tox+=dx[i]; toy+=dy[i];
                if (!check(tox,toy)) break;
                if (a[tox][toy]==4 || a[tox][toy]==3) {
                    int val=a[tox][toy];
                    a[tox][toy]=0;
                    int tox2=tox+dx[i],toy2=toy+dy[i];
                    while (check(tox2,toy2)) {
                        auto node=eatByQueen(tox2,toy2);
                        node.addDraught(tox,toy,val);
                        res=res.maxResult(res,node);
                    }
                    a[tox][toy]=val;
                }
            }
        }

        if (res.count==0) {
            if (checkForNotAte(x,y)) res.lose_queen=true;
        }
    }
    pair<bool, EatResult> eat(int x, int y) {
        EatResult res;
        vector<vector<bool>> used(8,vector<bool>(8,false));
        if (a[x][y]==2) {
            QueenEatResult res2=eatByQueen(x,y);
            res=EatResult(res2);
        }
        else if (a[x][y]==1) res=eatByNormal(x,y, used);
        else return {false, EatResult()};

        if (res.count==0) return {false,EatResult()};
        else return {true,res};
    }

    static int getRandDirection() {
        if (rand()%2==0) return 1;
        else return -1;
    }
    bool checkForNotAte(int x, int y) {
        bool is_ate=false;
        // проверка чтобы не съела простая пешка
        forn(k,4) {
            int tox2=x+dx[k],toy2=y+dy[k];
            if (check(tox2,toy2) && a[tox2][toy2]==3 && a[x-dx[k]][y-dy[k]]==0) is_ate=true;
            if (check(tox2,toy2) && a[tox2][toy2]==3 && x-dx[k]==x && y-dy[k]==y) is_ate=true;
        }
        // проверка чтобы не съела дамка
        forn(k,4) {
            int tox2=x,toy2=y;
            while (check(tox2,toy2)) {
                if (a[tox2][toy2]==4) is_ate=true;
                if (a[tox2][toy2]!=0) break;
                tox2+=dx[k];
                toy2+=dy[k];
            }
        }
        return is_ate;
    }
    bool moveDraught(int x, int y) {
        if(a[x][y]==1) {
            vector<pii> d={{-1,-1},{-1,1}};
            random_shuffle(all(d));
            forn(i,d.size()) {
                int tox=x+d[i].ff,toy=y+d[i].ss;
                if (check(tox,toy) && a[tox][toy]==0) {
                    bool is_ate=checkForNotAte(tox,toy);
                    if (!is_ate) {
                        Moves moves=Moves({x,y},{{tox,toy}});
                        updateGrid(moves);
                        moves.print();
                        return true;
                    }
                }
            }
            return false;
        } else if (a[x][y]==2) {
            vector<pii> d={{-1,-1},{1,1},{-1,1},{1,-1}};
            random_shuffle(all(d));
            forn(i,4) {
                int tox=x+d[i].ff, toy=y+d[i].ss;
                while (check(tox,toy)) {
                    if (a[tox][toy]==0) {
                        bool is_ate=checkForNotAte(tox,toy);
                        if (!is_ate) {
                            Moves moves=Moves({x,y},{{tox,toy}});
                              updateGrid(moves);
                            moves.print();
                            return true;
                        }
                    } else break;
                }
            }
        } else return false;
    }
    bool moveToQueen(int x, int y) {
        if (a[x][y]!=1) return false;
        forn(i,4) {
            int tox=x+dx[i],toy=y+dy[i];
            if (check(tox,toy) && tox==0 && a[tox][toy]==0) {
                a[x][y]=0;
                a[tox][toy]=2;
                Moves moves=Moves({x,y},{{tox,toy}});
                moves.print();
                return true;
            }
        }
        return false;
    }
    bool tryRandomMove(int x, int y) {
        if (a[x][y]==1) {
            vector<pii> d={{-1,1},{-1,-1}};
            forn(i,2) {
                int tox=x+d[i].ff, toy=y+d[i].ss;
                if (check(tox,toy) && a[tox][toy]==0) {
                    Moves moves=Moves({x,y},{{tox,toy}});
                    updateGrid(moves);
                    moves.print();
                    return true;
                }
            }
        }
        else if (a[x][y]==2) {
            forn(i,4) {
                int tox=x+dx[i], toy=y+dy[i];
                if (check(tox,toy) && a[tox][toy]==0) {
                    Moves moves=Moves({x,y},{{tox,toy}});
                    updateGrid(moves);
                    moves.print();
                    return true;
                }
            }
        }
        return false;
    }

    void updateGrid(Moves moves) {
        pii c=moves.start;
        int fig=a[c.ff][c.ss];
        forx(i,moves.moves) {
            int dix=(i.ff-c.ff>0? 1:-1), diy=(i.ss-c.ss>0? 1:-1);
            while (c!=i) {
                a[c.ff][c.ss]=0;
                c.ff+=dix;
                c.ss+=diy;
            }
            a[c.ff][c.ss]=fig;
        }
    }
} g;


void solve() {
    string clr; cin>>clr;

    Moves cur;
    if (clr=="white") {
        cur=Moves({5,6},{{4,7}});
        g.updateGrid(cur);
        cur.print();
    }

    while(true) {
        cur.read();
        if (cur.start.ff==-1) return;
        g.updateGrid(cur);
        // finding for maximum eat count
        EatResult eat_max;
        forn(i,g.d) {
            forn(j,g.d) {
                auto eat_try=g.eat(i,j);
                if (eat_try.ff)
                    eat_max=eat_max.maxResult(eat_max, eat_try.ss);
            }
        }
        if (eat_max.count!=0) {
            reverse(all(eat_max.path));
            eat_max.print();
            g.updateGrid(eat_max.getMoves());
            continue;
        }

        // checking for making a queen
        bool is_moved=false;
        forn(i,g.d) {
            forn(j,g.d) {
                auto x=g.moveToQueen(i,j);
                if (x) { is_moved=true; break; }
            }
            if (is_moved) break;
        }
        if (is_moved) continue;

        // checking for random valid move without eating our draught
        forn(i,g.d) {
            forn(j,g.d) {
                if (g.moveDraught(i,j)) { is_moved=true; break; }
            }
            if (is_moved) break;
        }
        if (is_moved) continue;

        // in any other way just move random draught forward
        bool done=false;
        forn(i,g.d) {
            forn(j,g.d) {
                auto x=g.tryRandomMove(i,j);
                if (x) done=true;
                if (done) break;
            }
            if (done) break;
        }
        if (done) continue;
    }

}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

//    ll _; cin>>_; while (_--) solve(),cout<<endl;
    solve();

    return 0;
}
