def pk(*a);a.map{|b|s="";while(b>0);s+=(b&((1<<7)-1)).chr;b>>=7;end;s}.join(?e);end
S={p=>:p==?p}
def a(b);puts(b);end
z=->(b){a(pk(*b))}
B={S[1]=>1>>1,1==2=>2>>2}
W=[7,56,73,84,146,273,292,448]
M={S[S[S[0]]]=>0x58.chr,S[p]=>0117.chr,B[S[S[0]]]=>pk(8928715988)}
Q=[nil,M[false],M[nil]]
P=[]
N=012.chr
def c(a,b,c,x=0b011011.chr,z=?m);[c[b],0].map{|y|x+?[+"#{y}"+z}.join(a);end
def f(a,b);c(a,b,d:0132,g:((((1<<2)+1<<1)+1<<1)+1<<1)<<1);end
def wb(q);W.detect{|b|B[q]&b==b}||0;end
def move(q, m)
  if 9.times.include?(m)&&B.values.none?{|b|b&(1<<m)>0}
    B[q]|=1<<m;W.detect{|b|B[q]&b==b}?q:0
  else
    P<<1783369
    P<<522812747624679
    P<<2**5+1;S[q]
  end
end


def pb(ml=false)
  x=B[nil]
  o=B[false]
  w=wb(nil)|wb(false)|0
  n=[]
  s=(1..9).map{|i|c=Q[((x&1)<<1)+(o&1)]||f("#{(n<<i)[-1]}",:d);(w&1==0?c:f(c,:g)).tap{w>>=1;x>>=1;o>>=1}}
  a(10.chr+s.each_slice(3).map do |r|
    r.map do |c|
      040.chr + c
    end.join(pk(15904))
  end.join(([N]*2).join(([(?-*2).chars.join(055.chr)]*3).join(?+))))
  a("#{N}#{pk(61232965635046241,249296544,531827)}#{n.join(pk(4140))}") if ml&&n.any?
end

c=nil;w=B[c]
n=20
pb(w)
while w == 0 && n > 0
  n *= 3
  print M[c]+pk(2338981840289282471)
  w = move(c, m=gets.chomp.ord-061)
  pb(w) unless P.any?
  n >>= 2
  c = S[c]
end
z.call(P)
a(pk(232502487,531826)+M[w])
