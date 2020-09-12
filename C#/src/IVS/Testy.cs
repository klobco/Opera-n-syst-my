using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using MathLibrary;

namespace IVS
{
	/// <summary>
	/// Trida testu
	/// </summary>
    public partial class Testy : Form
    { //Kod pro testy

        static int chyby = 0;//pocet chyb

        /// <summary>
        /// Vytvoreni noveho objektu, provedeni testu
        /// </summary>
        public Testy()
        {
            InitializeComponent();

            int chybneokruhy = 0;

            richTextBox1.AppendText("::::::::::::::::::::::::::::::\r\n::Testy matematicke knihovny::\r\n::::::::::::::::::::::::::::::\r\n\r\n");

            //testy pro plus
            richTextBox1.AppendText(":::Testy Soucet:::");
            chyby = 0;
            ExpectEQ(4.5, math.Soucet(2, 2.5));
            ExpectEQ(4.5, math.Soucet(2.5, 2));
            ExpectNEQ(4.5, math.Soucet(2, 2.500001));
            ExpectNEQ(4.5, math.Soucet(2.500001, 2));
            ExpectNEQ(4.5, math.Soucet(10, 30));
            richTextBox1.AppendText("\r\n:::Konec testu Soucet");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");

            //testy pro odcitani
            richTextBox1.AppendText(":::Testy Rozdil:::");
            chyby = 0;
            ExpectEQ(4.5, math.Rozdil(6.5, 2));
            ExpectEQ(4.5, math.Rozdil(5.052345, 0.552345));
            ExpectNEQ(4.5, math.Rozdil(2, 6.5));
            ExpectNEQ(4.5, math.Rozdil(0.552345, 5.052345));
            ExpectNEQ(4.5, math.Rozdil(1534, 13));
            ExpectEQ(4.5, math.Rozdil(4, -0.5));
            richTextBox1.AppendText("\r\n:::Konec testu Rozdil:::");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");

            //testy pro nasobení
            richTextBox1.AppendText(":::Testy Nasob:::");
            chyby = 0;
            ExpectEQ(4.5, math.Nasob(2.25, 2));
            ExpectEQ(4.5, math.Nasob(2, 2.25));
            ExpectNEQ(4.5, math.Nasob(2.25, 2.000001));
            ExpectEQ(-13, math.Nasob(6.5, -2));
            ExpectNEQ(13, math.Nasob(6.5, -2));
            richTextBox1.AppendText("\r\n:::Konec testu Nasob:::");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");

            //testy pro dělení
            richTextBox1.AppendText(":::Testy Podil:::");
            chyby = 0;
            ExpectEQ(-2, math.Podil(13, -6.5));
            ExpectEQ(4.5, math.Podil(-9, -2));
            ExpectNEQ(4.5, math.Podil(9, -2));
            ExpectThrow(math.Podil,5 , 0.0);
            ExpectThrow(math.Podil, 0, 0.0);
            ExpectThrow(math.Podil, 5, 0.0000);
            richTextBox1.AppendText("\r\n:::Konec testu Podil:::");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");

            //testy pro faktorial
            richTextBox1.AppendText(":::Testy Faktorial:::");
            chyby = 0;
            ExpectEQ(120, math.Faktorial(5));
            ExpectEQ(1, math.Faktorial(0));
            ExpectNEQ(13, math.Faktorial(7));
            ExpectEQ(1, math.Faktorial(1));
            ExpectEQ(2, math.Faktorial(2));
            ExpectThrow(math.Faktorial, -1);
            ExpectThrow(math.Faktorial, 4.5);
            ExpectThrow(math.Faktorial, -7);
            richTextBox1.AppendText("\r\n:::Konec testu Faktorial:::");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");

            //testy pro Umocnit
            richTextBox1.AppendText(":::Testy Umocnit:::");
            chyby = 0;
            ExpectEQ(25, math.Umocnit(5,2));
            ExpectEQ(125, math.Umocnit(5, 3));
            ExpectNEQ(25, math.Umocnit(2, 5));
            ExpectEQ(32, math.Umocnit(2, 5));
            ExpectEQ(1024, math.Umocnit(2, 10));
            ExpectEQ(1, math.Umocnit(5, 0));
            ExpectThrow(math.Umocnit, 10,  -1.0);
            ExpectThrow(math.Umocnit, 2, 0.5);
            ExpectThrow(math.Umocnit, 2, 0.2);
            richTextBox1.AppendText("\r\n:::Konec testu Umocnit:::");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");

            //testy pro Odmocnina
            richTextBox1.AppendText(":::Testy Odmocnina:::");
            chyby = 0;
            ExpectEQ(5, math.Odmocnina(25, 2));
            ExpectEQ(5, math.Odmocnina(125, 3));
            ExpectNEQ(25, math.Odmocnina(2, 5));
            ExpectEQ(2, math.Odmocnina(1024, 10));
            ExpectThrow(math.Odmocnina, 10, -1);
            ExpectThrow(math.Odmocnina, -1, 2);
            ExpectThrow(math.Odmocnina, -1, 0);
            ExpectNoThrow(math.Odmocnina, 0, 3);
            richTextBox1.AppendText("\r\n:::Konec testu Odmocnina:::");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");

            //testy pro Umocnit

            richTextBox1.AppendText(":::Testy Tangens:::");
            chyby = 0;
            ExpectEQ(0.6483608274590866, math.Tangens(10));
            ExpectEQ(2.237160944224742, math.Tangens(20));
            ExpectEQ(0, math.Tangens(0));
            ExpectNEQ(16331239353195370, math.Tangens(Math.PI/2));
            richTextBox1.AppendText("\r\n:::Konec testu Tangens:::");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");

            //testy pro odchylku
            List<double> pole = new List<double>(){1, 2, 3, 4, 5, 6};
            richTextBox1.AppendText(":::Testy Odchylky:::");
            chyby = 0;
            ExpectEQ(1.87082869339, math.odchylka_s(6, pole));
            pole.Clear();
            pole.Add(-3); pole.Add(4); pole.Add(5); pole.Add(-11); pole.Add(6);
            ExpectEQ(7.1902712049, math.odchylka_s(5, pole));
            pole.Clear();
            pole.Add(4); pole.Add(1); pole.Add(-5); pole.Add(-111); pole.Add(54);
            ExpectEQ(60.4756149204, math.odchylka_s(5, pole));
            pole.Clear();
            pole.Add(0); pole.Add(0); pole.Add(0); pole.Add(0); pole.Add(0);
            ExpectEQ(0, math.odchylka_s(5, pole));
            ExpectThrow(math.odchylka_s, 6, pole);
            ExpectThrow(math.odchylka_s, 0, pole);

            richTextBox1.AppendText("\r\n:::Konec testu Odchylky:::");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");

            //testy pro Zpracovani vyrazu
            // Zpracovat_Vyraz(string vyraz)
            richTextBox1.AppendText(":::Testy Zpracovani vyrazu:::");
            chyby = 0;
            ExpectThrow(math.Zpracovat_Vyraz,"5//4");
            ExpectNoThrow(math.Zpracovat_Vyraz, "5++4");
            ExpectNoThrow(math.Zpracovat_Vyraz, "5--4");
            ExpectNoThrow(math.Zpracovat_Vyraz, "5+-4");
            ExpectThrow(math.Zpracovat_Vyraz, "5**4");
            ExpectNoThrow(math.Zpracovat_Vyraz, "5*-4");
            ExpectNoThrow(math.Zpracovat_Vyraz, "5*+4");
            ExpectNoThrow(math.Zpracovat_Vyraz, "5+-4");
            ExpectThrow(math.Zpracovat_Vyraz, "5*/4");
            ExpectNoThrow(math.Zpracovat_Vyraz, "5+4*7-2*5+40*2");
            ExpectNoThrow(math.Zpracovat_Vyraz, "5+4+2+9*4/5/5/5/5/5-4*3+2*4*7*5+3+4+7-14");
            ExpectEQ(4.2,Convert.ToDouble(math.Zpracovat_Vyraz("2√4+2,2")));
            ExpectEQ(-11.62, Convert.ToDouble(math.Zpracovat_Vyraz("4,7*2/5+3,5-4*2√25+3")));
            ExpectEQ(6.5, Convert.ToDouble(math.Zpracovat_Vyraz("3,2*3√125/4/2-3*4/8-3*-2")));
            ExpectEQ(2.5, Convert.ToDouble(math.Zpracovat_Vyraz("10√1024*6+3-4*25/8")));
            richTextBox1.AppendText("\r\n:::Konec testu Zpracovani vyrazu:::");
            if (chyby != 0)
            {
                chybneokruhy++;
            };
            richTextBox1.AppendText("Pocet Chyb:" + chyby + ":::\r\n\r\n");



            richTextBox1.AppendText(":::::::::::::::::::::::::::::\r\n:::Pocet chybnych funkci:" + chybneokruhy + ":::\r\n");
            richTextBox1.AppendText("::::::::::::::::::::::::::::::::::::\r\n::Konec testu matematicke knihovny::\r\n::::::::::::::::::::::::::::::::::::\r\n\r\n");
        }

        /// <summary>
		/// Očekává rovnost, výsledek vypíše
		/// </summary>
		/// <param name="a">double</param>
        /// <param name="b">double</param>
        void ExpectEQ(double a, double b)
        {
            double odchylka = 0.0000000001;
            double rozdil = Math.Abs(a - b);
            if (rozdil > odchylka)
            {
                chyby++;
                richTextBox1.AppendText("\r\nChybaEQ ");
            }
            else
            {
                richTextBox1.AppendText("\r\nEQ ");
            }
            richTextBox1.AppendText("Ocekavany vysledek:" + a + " / Realny vysledek:" + b);
        }

        /// <summary>
        /// Očekává nerovnost, výsledek vypíše
        /// </summary>
        /// <param name="a">double</param>
        /// <param name="b">double</param>
        void ExpectNEQ(double a, double b)
        {
            double odchylka = 0.0000000001;
            double rozdil = Math.Abs(a - b);
            if (rozdil < odchylka)
            {
                chyby++;
                richTextBox1.AppendText("\r\nChybaNEQ ");
            }
            else
            {
                richTextBox1.AppendText("\r\nNEQ ");
            }
            richTextBox1.AppendText("Ocekavany vysledek:" + a + " / Realny vysledek:" + b);
        }
        /// <summary>
        /// Pro předání funkce jako parametr
        /// </summary>
        /// <param name="a">double</param>
        /// <returns>int</returns>
        delegate int Function(double a);
        /// <summary>
        /// Pro předání funkce jako parametr
        /// </summary>
        /// <param name="a">double</param>
        /// <param name="b">double</param>
        /// <returns>double</returns>
        delegate double Function2(double a, double b);
        /// <summary>
        /// Pro předání funkce jako parametr
        /// </summary>
        /// <param name="a">double</param>
        /// <param name="b">int</param>
        /// <returns>double</returns>
        delegate double Function3(double a, int b);
        /// <summary>
        /// Pro předání funkce jako parametr
        /// </summary>
        /// <param name="N">int, pocet prvku</param>
        /// <param name="pole">List<double></param>
        /// <returns>double</returns>
        delegate double Function4(int N, List<double> pole);

        /// <summary>
        /// Pro předání funkce jako parametr
        /// </summary>
        /// <param name="s">string</param>
        /// <returns>string</returns>
        delegate string Function5(string s);

        /// <summary>
        /// Očekává vyjimku, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici double ktera bere dva double parametry</param>
        /// <param name="a">double</param>
        /// <param name="b">double</param>        
        void ExpectThrow (Function2 funkce,double a,double b)
        {
            try
            {
                funkce(a, b);
                chyby++;
                richTextBox1.AppendText("\r\nChybaThrow zadane parametry:"+a + " "+b);
            }
            catch
            {
                richTextBox1.AppendText("\r\nThrow zadane parametry:" + a + " " + b);
            }
        }

        /// <summary>
        /// Očekává vyjimku, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici string ktera bere string</param>
        /// <param name="s">string</param>      
        void ExpectThrow(Function5 funkce,string s)
        {
            try
            {
                funkce(s);
                chyby++;
                richTextBox1.AppendText("\r\nChybaThrow zadany parametr:" + s);
            }
            catch
            {
                richTextBox1.AppendText("\r\nThrow zadany parametr:"+s);
            }
        }

        /// <summary>
        /// Očekává vyjimku, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici double ktera bere dva parametry</param>
        /// <param name="N">int, pocet prvku pole</param>
        /// <param name="pole">List<double></param>        
        void ExpectThrow(Function4 funkce, int N, List<double> pole)
        {
            try
            {
                funkce(N, pole);
                chyby++;
                richTextBox1.AppendText("\r\nChybaThrow zadane parametry:" + N + " pole");
            }
            catch
            {
                richTextBox1.AppendText("\r\nThrow zadane parametry:" + N + " pole");
            }
        }


        /// <summary>
        /// Očekává vyjimku, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici double ktera bere double a int parametry</param>
        /// <param name="a">double</param>
        /// <param name="b">int</param>
        void ExpectThrow(Function3 funkce, double a, int b)
        {
            try
            {
                funkce(a, b);
                chyby++;
                richTextBox1.AppendText("\r\nChybaThrow zadane parametry:" + a + " " + b);
            }
            catch
            {
                richTextBox1.AppendText("\r\nThrow zadane parametry:" + a + " " + b);
            }
        }

        /// <summary>
        /// Očekává vyjimku, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici int, ktera bere double parametr</param>
        /// <param name="a">double</param>
        void ExpectThrow(Function funkce, double a)
        {
            try
            {
                funkce(a);
                chyby++;
                richTextBox1.AppendText("\r\nChybaThrow zadany parametr:" + a);
            }
            catch
            {
                richTextBox1.AppendText("\r\nThrow zadany parametr:" +a);
            }
        }

        /// <summary>
        /// Očekává ze nenastane vyjimka, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici string ktera bere string</param>
        /// <param name="s">string</param>      
        void ExpectNoThrow(Function5 funkce, string s)
        {
            try
            {
                funkce(s);
                richTextBox1.AppendText("\r\nNoThrow zadany parametr:" + s);
            }
            catch
            {
                chyby++;
                richTextBox1.AppendText("\r\nChybaNoThrow zadany parametr:" + s);
            }
        }

        /// <summary>
        /// Očekává ze nenastane vyjimka, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici double ktera bere dva parametry</param>
        /// <param name="N">int, pocet prvku pole</param>
        /// <param name="pole">List<double></param>  
        void ExpectNoThrow(Function4 funkce, int N, List<double> pole)
        {
            try
            {
                funkce(N, pole);
                richTextBox1.AppendText("\r\nNoThrow zadane parametry:" + N + " pole");
            }
            catch
            {
                chyby++;
                richTextBox1.AppendText("\r\nChybaNoThrow zadane parametry:" + N + " pole");
            }
        }

        /// <summary>
        /// Očekává ze nenastane vyjimka, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici double ktera bere dva double parametry</param>
        /// <param name="a">double</param>
        /// <param name="b">double</param>
        void ExpectNoThrow(Function2 funkce, double a, double b)
        {
            try
            {
                funkce(a, b);
                richTextBox1.AppendText("\r\nNoThrow zadane parametry:" + a + " " + b);
            }
            catch
            {
                chyby++;
                richTextBox1.AppendText("\r\nChybaNoThrow zadane parametry:" + a + " " + b);
            }
        }

        /// <summary>
        /// Očekává ze nenastane vyjimka, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici double ktera bere double a int parametry</param>
        /// <param name="a">double</param>
        /// <param name="b">int</param>
        void ExpectNoThrow(Function3 funkce, double a, int b)
        {
            try
            {
                funkce(a, b);
                richTextBox1.AppendText("\r\nNoThrow zadane parametry:" + a + " " + b);
            }
            catch
            {
                chyby++;
                richTextBox1.AppendText("\r\nChybaNoThrow zadane parametry:" + a + " " + b);
            }
        }

        /// <summary>
        /// Očekává ze nenastane vyjimka, výsledek vypíše
        /// </summary>
        /// <param name="funkce">funkce vracejici int, ktera bere double parametr</param>
        /// <param name="a">double</param>
        void ExpectNoThrow(Function funkce, double a)
        {
            try
            {
                funkce(a);
                richTextBox1.AppendText("\r\nNoThrow zadany parametr:" + a);
            }
            catch
            {
                chyby++;
                richTextBox1.AppendText("\r\nChybaNoThrow zadany parametr:" + a);
            }
        }
    }
}
