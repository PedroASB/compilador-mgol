# Códigos de Teste

## Caractere não esperado
### Linha 2, Coluna 7

leia B;
1.2e+-2
escreva "Digite A:";
fimse

## Comentário não finalizado - Linha 4, Coluna 7

leia B;
{comentario
escreva "Digite A:";
fimse

## Literal não finalizado - Linha 14, Coluna 10

inicio
varinicio
literal A,B;
inteiro B;
inteiro D;
real C ;
varfim;
escreva B;
leia B;
escreva "Digite A;
leia A;
se(B>2)
entao
se(B<=4)

## Caractere não esperado
### Linha 4, Coluna 8
### Linha 6, Coluna 7

inicio
varinicio
literal A,B;
inteir.o B;
inteiro D;
real _underlineNoInicio C ;

## Produz token de erro (um caractere)

leia B;
1.2e+@2
escreva "Digite A:";
fimse

## Código Correto
inicio
varinicio
literal A,B;
inteiro B;
inteiro D;
real C ;
varfim;
escreva "Digite B:";
leia B;
escreva "Digite A:";
leia A;
se(B>2)
entao
se(B<=4)
entao
escreva "B esta entre 2 e 4";
fimse
fimse
B<-B+1;
B<-B+2;
B<-B+3;
D<-B;
C<-5.0;
repita (B<5)
C<-B+2;
escreva C;
B<-B+1;
fimrepita
escreva "\nB=\n";
escreva D;
escreva "\n";
escreva C;
escreva "\n";
escreva A;
fim
