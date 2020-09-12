#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <errno.h>
#include <semaphore.h>
#include <string.h>
#include <ctype.h>
#include <time.h>
#include <limits.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>

#define WAIT(count) {for (unsigned long i = 0; i < count; ++i) waitpid(-1, NULL, 0);}
#define MAP(pointer) {(pointer) = mmap(NULL,sizeof(*(pointer)), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);}
#define UNMAP(pointer) {munmap((pointer), sizeof((pointer)));}

unsigned int ran_num(unsigned int max);
void clean();
int inicializacia();
void make_rid(int c);
void make_bus(int delay, int capacity);
void rider_generator(int R, int delay);
void kontrola(int argc, char*argv[]);

bool jazda = true;
int R;
int C;
unsigned int ART; 
unsigned int ABT;
FILE *proj2;

//miesto pre semafory a shared premenne
int *proces_poc = 0;
int *zastavka_lud = 0;
int *ludia = 0;
int *vyt_rid = 0;
int *odv_lud = 0;
int *boarding = 0;

sem_t *vyp;
sem_t *end3;
sem_t *end2;
sem_t *end;
sem_t *vypis;
sem_t *ukoncenie;
sem_t *autobus;

//koniec miesta pre semafory a shared premenne


int main(int argc, char *argv[])
{
clean();
kontrola(argc, argv);
if(inicializacia() != 0)
{
    fprintf(stderr,"Nezdarila sa inicializacia!\n");
    clean();
    exit(1);
}
*vyt_rid=0;
char *tmp;
long test;
*boarding = 1;
R = atoi(argv[1]);
C = atoi(argv[2]);
test = strtoul(argv[3], &tmp, 10);
ART = (unsigned int) test;
test = strtoul(argv[4], &tmp, 10);
ABT = (unsigned int) test;

pid_t BUS = fork();
if(BUS == 0)
{
    make_bus(ABT, C);
    exit(0);
}
else
{
    pid_t GEN = fork();
    if(GEN == 0)
    {
        rider_generator(R, ART);
        exit(0);
    }
    else
    {
    WAIT(2);
    sem_wait(end);
    clean();
    return 0;
    }
}
}

//proces na vytvorenie a spracovanie autobusu
void make_bus(int delay, int capacity)
{
    sem_wait(vypis);
    fprintf(proj2, "%d\t : BUS\t : start\n", ++(*proces_poc));
    sem_post(vypis);
    while(jazda == true)
    {
        sem_wait(vypis);
        fprintf(proj2, "%d\t : BUS\t : arrival\n", ++(*proces_poc));
        sem_post(vypis);
        
        sem_post(autobus);
        sem_wait(autobus);
        int ukon=0;
        if(*zastavka_lud != 0)
        {
            sem_wait(vypis);
            fprintf(proj2, "%d\t : BUS\t : start boarding: %d\n", ++(*proces_poc),(*zastavka_lud));
            sem_post(vypis);
            int zast=(*zastavka_lud);
            for (int g = 0; g < zast; g++)
            {
                if(g >= capacity || (*zastavka_lud) == 0)
                {
                    break;
                }
                sem_wait(vypis);
                sem_post(end2);
                sem_wait(end3);
                //fprintf(proj2, "%d\t : RID %d\t : boarding\n", ++(*proces_poc),(*boarding));
                (*boarding)++;
                (*ludia)++;
                ukon++;
                *zastavka_lud-=1;
                sem_post(vypis);
            }
            sem_wait(vypis);
            fprintf(proj2, "%d\t : BUS\t : end boarding: %d\n", ++(*proces_poc),(*zastavka_lud));
            sem_post(vypis);
        }
        
        sem_wait(vypis);
        fprintf(proj2, "%d\t : BUS\t : depart\n", ++(*proces_poc));
        sem_post(vypis);
        sem_post(autobus);
        usleep(ran_num(delay)*1000);
        sem_wait(autobus);
        sem_wait(vypis);
        fprintf(proj2, "%d\t : BUS\t : end\n", ++(*proces_poc));
        sem_post(vypis);
        for(int h=0 ; h < ukon ; h++)
        {
            sem_post(ukoncenie);
        }
        if((*ludia) >= R) jazda = false;
    }
    sem_wait(vypis);
    fprintf(proj2, "%d\t : BUS\t : finish\n", ++(*proces_poc));
    sem_post(vypis);
    sem_post(end);
    exit(0);
}

//vytvorenie rideru číslo R
void make_rid(int c)
{
    sem_wait(vyp);
    sem_wait(vypis);
    fprintf(proj2, "%d\t : RID %d\t : start\n", ++(*proces_poc),c+1);
    sem_post(vypis);

    sem_wait(autobus);


    sem_wait(vypis);
    fprintf(proj2, "%d\t : RID %d\t : enter: %d\n", ++(*proces_poc),c+1,++(*zastavka_lud));
    sem_post(vypis);
    sem_post(vyp);

    sem_post(autobus);

    sem_wait(end2);
    fprintf(proj2, "%d\t : RID %d\t : boarding\n", ++(*proces_poc),(c+1));
    sem_post(end3);

    sem_wait(ukoncenie);
    
    sem_wait(vypis);
    fprintf(proj2, "%d\t : RID %d\t : finish\n", ++(*proces_poc),c+1);
    sem_post(vypis);

    //sem_wait(end2);
    exit(0);
}

//upratuje všetky semafory a shared pamäť
void clean()
{
    //uvolnenie sdilenych prom.
    UNMAP(zastavka_lud)
    UNMAP(proces_poc)
    UNMAP(ludia)
    UNMAP(vyt_rid)
    UNMAP(odv_lud)
    UNMAP(boarding)

    //uvolnenie semaforov


    sem_close(vyp);
    sem_unlink("xklobu03.ios.proj2.vyp");
    sem_close(end3);
    sem_unlink("xklobu03.ios.proj2.end3");
    sem_close(end2);
    sem_unlink("xklobu03.ios.proj2.end2");
    sem_close(end);
    sem_unlink("xklobu03.ios.proj2.end");
    sem_close(vypis);
    sem_unlink("xklobu03.ios.proj2.vypis");
    sem_close(ukoncenie);
    sem_unlink("xklobu03.ios.proj2.ukoncenie");
    sem_close(autobus);
    sem_unlink("xklobu03.ios.proj2.semafor");

    //zavretie suboru

    if (proj2 != NULL)
    {
        fclose(proj2);
    }
}

//inicializuje všetky potrebné premenné a pamäť
int inicializacia()
{
    proj2 = fopen("proj2.out", "w");
    setbuf(proj2, NULL);
    MAP(odv_lud)
    MAP(vyt_rid)
    MAP(zastavka_lud)
    MAP(proces_poc)
    MAP(ludia)
    MAP(boarding)


    if((vyp = sem_open("xklobu03.ios.proj2.vyp", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
    {
        return -1;
    }
    if((end3 = sem_open("xklobu03.ios.proj2.end3", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
    {
        return -1;
    }
    if((end2 = sem_open("xklobu03.ios.proj2.end2", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
    {
        return -1;
    }
    if((end = sem_open("xklobu03.ios.proj2.end", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
    {
        return -1;
    }
    if((vypis = sem_open("xklobu03.ios.proj2.vypis", O_CREAT | O_EXCL, 0666, 1)) == SEM_FAILED)
    {
        return -1;
    }
    if((autobus = sem_open("xklobu03.ios.proj2.semafor", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
    {
        return -1;
    }
    if((ukoncenie = sem_open("xklobu03.ios.proj2.ukoncenie", O_CREAT | O_EXCL, 0666, 0)) == SEM_FAILED)
    {
        return -1;
    }
    return 0;
}

//generuje riders 
void rider_generator(int R, int delay)
{
    for (int i = 0; i < R; i++)
    {
        pid_t RID = fork();
        if (RID == 0)
        {
            make_rid(i);
        }
        usleep(ran_num(delay) * 1000);
    }
    //sem_post(end2);
    exit(0);
}

unsigned int ran_num(unsigned int max)
{
    if (max == 0)
        return 0;
    srand((unsigned int) time(NULL)); 
    return rand() % max; 
}

void kontrola(int argc, char*argv[])
{
    if (argc != 5)
    {
        fprintf(stderr,"Chybný počet argumentov!\n");
        exit(0);
    }
    for(int i=1;i<argc;i++)
    {
        int skut=0;
        int cis=strlen(argv[i]);
        for(int j=0;j<=cis;j++)
        {
            if(argv[i][j] > 47 && argv[i][j] < 58)
            {
                skut++; 
            }
        }
        if(skut != cis)
        {
        fprintf(stderr,"Chyba, zadané argumenty musia byť čísla!\n");
        exit(0);
        }
    }
    if(atoi(argv[2]) <= 0)
    {
        fprintf(stderr,"Chyba, zadaný argument 2 musí byť viac ako 0!\n");
        exit(0);
    }
    if(atoi(argv[3]) < 0 || atoi(argv[3]) > 1000)
    {
        fprintf(stderr,"Chyba, zadaný argument 3 musí byť v rozmedzii 0-1000!\n");
        exit(0);
    }
    if(atoi(argv[4]) < 0 || atoi(argv[4]) > 1000)
    {
        fprintf(stderr,"Chyba, zadaný argument 4 musí byť v rozmedzii 0-1000!\n");
        exit(0);
    }
}
