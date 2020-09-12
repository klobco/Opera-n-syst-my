using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MathLibrary
{
	/// <summary>
	/// Trida math provadejici zakladni a porkocile mat operace. Umi i zpracovat vyraz bez zavorek.
	/// </summary>
	public class math
	{
		/// <summary>
		/// Testuje jestli zadane cislo je cele
		/// </summary>
		/// <param name="a"></param>
		/// <returns>Vraci True pokud je cislo cele, jinak false</returns>
		private static bool Test_Int(double a)
		{
			if ((a % 1) == 0)
				return true;
			else
				return false;
		}
		/// <summary>
		/// Soucet dvou cisel na vstupu
		/// </summary>
		/// <param name="a"></param>
		/// <param name="b"></param>
		/// <returns>Soucet vstupu</returns>
		public static double Soucet(double a, double b)
		{
			return a + b;
		}
		/// <summary>
		/// Rozdil dvou cisel na vstupu
		/// </summary>
		/// <param name="a"></param>
		/// <param name="b"></param>
		/// <returns>Rozdil vstupu</returns>
		public static double Rozdil(double a, double b)
		{
			return a - b;
		}
		/// <summary>
		/// Nasobeni dvou cisel na vstupu
		/// </summary>
		/// <param name="a"></param>
		/// <param name="b"></param>
		/// <returns>Nasobeni vstupu</returns>
		public static double Nasob(double a, double b)
		{
			return a * b;
		}
		/// <summary>
		/// Deleni dvou cisel na vstupu
		/// </summary>
		/// <param name="a"></param>
		/// <param name="b"></param>
		/// <exception cref="DivideByZeroException">Nastavi pri deleni nulou</exception>
		/// <returns>Deleni vstupu</returns>
		public static double Podil(double a, double b)
		{
			if (b == 0)
			{
				throw new DivideByZeroException();
			}
			return a / b;
		}
		/// <summary>
		/// Vypocita faktorial ze zadaneho cisla
		/// </summary>
		/// <param name="a"></param>
		/// <exception cref="ArgumentException">Pokud vstup neni prirozene cislo</exception>
		/// <returns>Faktorial vstupu</returns>
		public static int Faktorial(double a)
		{
			if (Test_Int(a) == false || a < 0 || a>31)
			{
				throw new ArgumentException();
			}
			if (a == 0 || a == 1)
			{
				return 1;
			}
			int f = 1;
			for (int i = 1; i <= a; i++)
			{
				f *= i;
			}
			return f;
		}
		/// <summary>
		/// Vypocita mocninu vstupniho cisla x umocneneho prirozenym cislem n
		/// </summary>
		/// <param name="x">Zaklad</param>
		/// <param name="n">Mocnitel</param>
		/// <exception cref="ArgumentException">N musi byt prirozene cislo</exception>
		/// <returns>Vraci N-tou mocninu vstupu</returns>
		public static double Umocnit(double x, double n)
		{
			if (Test_Int(n) == false || n < 0)
			{
				throw new ArgumentException();
			}
			if (n == 0)
			{
				return 1;
			}
			double vysledek = x;
			for (int i = 0; i < n - 1; i++)
			{
				vysledek = math.Nasob(vysledek, x);
			}
			return vysledek;
		}
		/// <summary>
		/// Pocita N-tou odmocninu pomoci kraceni mezi, presnost je 500 iteraci
		/// </summary>
		/// <param name="x">Zaklad</param>
		/// <param name="n">N-ta odmocnina</param>
		/// <returns>Vraci odmocninu s presnosti mensi jak 10^-10</returns>
		public static double Odmocnina(double x, int n)
		{
			if (Test_Int(n) == false || n < 0 || x < 0)
			{
				throw new ArgumentException();
			}
			double horni_mez = x;
			double dolni_mez = 0;

			double vysledek = x / 2;
			double k = math.Umocnit(vysledek, n);
			for (int i = 0; i < 500; i++)
			{
				if (k > x)
				{
					horni_mez = vysledek;
					vysledek = vysledek - ((horni_mez - dolni_mez) / 2);
				}
				else
				{
					dolni_mez = vysledek;
					vysledek = vysledek + ((horni_mez - dolni_mez) / 2);
				}
				k = math.Umocnit(vysledek, n);
			}
			return vysledek;
		}


		/// <summary>
		/// Vypocita Tangens pomoci metody zretezeneho zlomku, funguje presne jen v intervalu (-50,40)
		/// </summary>
		/// <param name="x">Uhel v radianech v rozsahu (-50,40)</param>
		/// <returns>´Vraci tangens s presnosti mensi jak 10^-8</returns>
		public static double Tangens(double x)
		{
			if (x < -50 || x > 40)
			{
				throw new ArgumentException();
			}
			double cf = 0;
			double b = 1;
			for (int i = 50; i > 0; i--)
			{
				double a = (2 * i - 1) / x;
				cf = b / (a - cf);
			}
			return cf;
		}
		/// <summary>
		/// Jednoduchy "wolfram", ktery zpracovava vyraz (+,-,*,/,^,√,!) podle priorit od nejvyssi (!,√,^,*,/,+,-), nepredpoklada nic jineho nez cisla a operatory ve spravnem formatu!
		/// </summary>
		/// <param name="vyraz">vyraz typu string</param>
		/// <returns>vraci vysledek jako jedno cislo typu string (pro kompatibilitu s dalsimi funkcemi)</returns>
		public static string Zpracovat_Vyraz(string vyraz)
		{
			while (vyraz.Contains('!'))
			{
				vyraz = Zpracovat_Sub_Vyraz(vyraz, '!', "+-*/^√!");
			}
			while (vyraz.Contains('√'))
			{
				vyraz=Zpracovat_Sub_Vyraz(vyraz, '√', "+-*/^√");
			}
			while (vyraz.Contains('^'))
			{
				vyraz = Zpracovat_Sub_Vyraz(vyraz, '^', "+-*/^");
			}
			while (vyraz.Contains('*'))
			{
				vyraz = Zpracovat_Sub_Vyraz(vyraz, '*', "+-*/");
			}
			while (vyraz.Contains('/'))
			{
				vyraz = Zpracovat_Sub_Vyraz(vyraz,'/', "+-/");
			}
			while (vyraz.Contains('+'))
			{
				vyraz = Zpracovat_Sub_Vyraz(vyraz, '+', "+-");
			}
			while (vyraz.Contains('-'))
			{
				vyraz = Zpracovat_Sub_Vyraz(vyraz, '-', "+-");
				int count = vyraz.Split('-').Length - 1;
				if (count == 1 && vyraz[0] == '-')
					return vyraz;
			}
			return vyraz;
		}

		/// <summary>
		/// Zpracovava sub vyraz, to znamena ze dostane cely vyraz, operator a zarážky
		/// najde ve vyrazu prvni vyskyt operatoru, pote naparsuje leve a prave cislo dle zarazek, provede mat operaci a vrati upraveny string
		/// </summary>
		/// <param name="vyraz"></param>
		/// <param name="op"></param>
		/// <param name="target"></param>
		/// <returns></returns>
		private static string Zpracovat_Sub_Vyraz(string vyraz, char op,string target)
		{

			int index = vyraz.IndexOf(op);
			char[] anyOf = target.ToCharArray();
			if (op == '+')
			{
				if (index == 0)
				{
					vyraz = vyraz.Remove(0, 1);
					return vyraz;
				}
			}
			if (op == '-')
			{
				int count = vyraz.Split('-').Length - 1;
				if (count == 1 && vyraz[0] == '-')
					return vyraz;


				if (index == 0)
				{
					index = vyraz.IndexOf('-', index + 1);
				}

				if (index == 0)
				{
					vyraz = vyraz.Remove(0, 1);
					return vyraz;
				}

			}
			
			int indexL = vyraz.Substring(0, index).LastIndexOfAny(anyOf);
			double cislo1;
			if (indexL == -1)
			{
				cislo1 = Convert.ToDouble(vyraz.Substring(indexL + 1, index - indexL - 1));
			}
			else
			{
				if (vyraz[indexL] == '-' || vyraz[indexL] == '+')
				{
					cislo1 = Convert.ToDouble(vyraz.Substring(indexL, index - indexL));
					indexL--;
				}
				else
				{
					cislo1 = Convert.ToDouble(vyraz.Substring(indexL + 1, index - indexL - 1));
				}
			}
			double cislo2=0;
			int indexR;
			if (op != '!')
			{
				string tmp = vyraz.Substring(index, vyraz.Length - index);

				if (tmp[1] == '-' || tmp[1] == '+')
				{
					indexR = tmp.IndexOfAny(anyOf, 2);
				}
				else
				{
					indexR = tmp.IndexOfAny(anyOf, 1);
				}

				if (indexR == -1)
					indexR = tmp.Length;
				tmp = tmp.Substring(1, indexR - 1);
				cislo2 = Convert.ToDouble(tmp);
				vyraz = vyraz.Remove(indexL + 1, indexR + index - indexL - 1);
			}
			else
			{
				vyraz = vyraz.Remove(indexL + 1,index - indexL );
			}
			
			
			double vys;

			switch (op)
			{
				case '+':
					{
						vys = Soucet(cislo1, cislo2);
						break;
					}
				case '-':
					{
						vys = Rozdil(cislo1, cislo2);
						break;
					}
				case '*':
					{
						vys = Nasob(cislo1, cislo2);
						break;
					}
				case '/':
					{
						vys = Podil(cislo1, cislo2);
						break;
					}
				case '^':
					{
						vys = Umocnit(cislo1, cislo2);
						break;
					}
				case '√':
					{
						vys = Odmocnina(cislo2, Convert.ToInt32(cislo1));
						break;
					}
				case '!':
					{
						vys = Faktorial(cislo1);
						break;
					}
				default:
					{
						throw new ArgumentException();
					}
				}
			vyraz = vyraz.Insert(indexL + 1, vys.ToString());
			if (vys >= 0)
			{
				vyraz = vyraz.Insert(indexL + 1, "+");
			}

			return vyraz;
		}
		/// <summary>
		/// Pocita vyberovou smerodatnou odchylku
		/// </summary>
		/// <param name="N">Pocet cisel</param>
		/// <param name="pole">Vstupni pole cisel</param>
		/// <returns></returns>
		public static double odchylka_s(int N, List<double> pole)
		{
			if (N <= 1)
				throw new ArgumentOutOfRangeException();
			double tmp = math.Podil(1, math.Rozdil(N, 1));
			double soucet = 0;
			for (int i = 0; i < N; i++)
			{
				soucet += math.Umocnit(pole[i], 2);
			}
			soucet -= math.Nasob(N, math.Umocnit(math.odchylka_x(N, pole), 2));
			tmp = math.Nasob(tmp, soucet);
			tmp = math.Odmocnina(tmp, 2);
			return tmp;
		}

		/// <summary>
		/// Mezivypocet vyberove smerodatne odchylky
		/// </summary>
		/// <param name="N"></param>
		/// <param name="pole"></param>
		/// <returns></returns>
		private static double odchylka_x(int N, List<double> pole)
		{
			double tmp = math.Podil(1, N);
			double soucet = 0;
			for (int i = 0; i < N; i++)
			{
				soucet += pole[i];
			}
			return math.Nasob(tmp, soucet);
		}

	}
}
