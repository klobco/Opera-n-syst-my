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
	/// Hlavni form aplikace
	/// </summary>
    public partial class Calculator : Form
    {
		/// <summary>
		/// Init komponent
		/// </summary>
        public Calculator()
        {
            InitializeComponent();
        }

        /// <summary>
        /// Pri nacteni formulare prepne focus na textbox
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void Calculator_Load(object sender, EventArgs e)
        {
            this.ActiveControl = textBox1;
        }

        /// <summary>
        /// textbox na zadávanie vstupov
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        /// <summary>
        /// Vloženie '0' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button4_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "0";
        }

        /// <summary>
        /// Vloženie '+' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button15_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "+";
        }

        /// <summary>
        /// vloženie '(' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button20_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "(";
        }

        /// <summary>
        /// Vloženie '1' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button1_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "1";
        }

        /// <summary>
        /// Vloženie '2' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button2_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "2";
        }

        /// <summary>
        /// Vloženie '3' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button3_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "3";
        }

        /// <summary>
        /// Vloženie '4' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button5_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "4";
        }

        /// <summary>
        /// Vloženie '5' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button6_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "5";
        }

        /// <summary>
        /// Vloženie '6' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button7_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "6";
        }

        /// <summary>
        /// Vloženie '7' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button8_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "7";
        }

        /// <summary>
        /// Vloženie '8' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button9_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "8";
        }

        /// <summary>
        /// Vloženie '9' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button10_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "9";
        }

        /// <summary>
        /// Vloženie ')' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button21_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + ")";
        }

        /// <summary>
        /// Vyčistenie textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button22_Click(object sender, EventArgs e)
        {
            textBox1.Clear();
        }

        /// <summary>
        /// Vloženie ',' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button19_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + ",";
        }

        /// <summary>
        /// Vloženie '-' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button16_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "-";
        }

        /// <summary>
        /// Vloženie 'x' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button17_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "*";
        }

        /// <summary>
        /// Vloženie '/' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button18_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "/";
        }

        /// <summary>
        /// Vloženie '^' do textového pola
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button12_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + "^";
        }

        /// <summary>
        /// funkcia spracuje a odstráni zátvorky
        /// </summary>
        /// <param name="text"></param>
        /// <returns></returns>
        protected string spracovanie_zatvorky(string text)
        {
            while (text.Contains('(') && text.Contains(')'))
            {
                string vysledok = "";
                int openIndex = 0;
                int closeIndex = 0;
                for (int i = 0; i < text.Length; i++)
                {
                    if (text[i] == '(')
                    {
                        openIndex = i;
                        if (char.IsDigit(text[i + 1]) == false && text[i + 1] != '-')
                        {
                            MessageBox.Show("Chyba vstupu! Zkontrolujte obsah zátvoriek!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                            return textBox1.Text;
                        }
                        if (i != 0 && char.IsDigit(text[i - 1]))
                        {
                            text = text.Insert(openIndex, "*");
                        }
                    }
                    if (text[i] == ')')
                    {
                        closeIndex = i;
                        string zatvorka = text.Substring(openIndex + 1, closeIndex - openIndex - 1);
                        text = text.Remove(openIndex, closeIndex - openIndex + 1);
                        try
                        {
                            vysledok = math.Zpracovat_Vyraz(zatvorka);
                        }
                        catch
                        {
                            MessageBox.Show("Chyba vstupu! Zkontrolujte znaménka!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                            return textBox1.Text;
                        }
                        text = text.Insert(openIndex, vysledok);
                        i = 0;
                    }
                }
            }
			if (Vstup(text) == false)
			{
				return textBox1.Text; 
			}
			try
            {
                text = math.Zpracovat_Vyraz(text);
            }
            catch
            {
                MessageBox.Show("Chyba vstupu! Zkontrolujte znaménka!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return textBox1.Text;
            }
            return text;
        }

        /// <summary>
        /// Funkcia zistí či je vstup korektný
        /// </summary>
        /// <param name="vstup"></param>
        /// <returns></returns>
        protected bool Vstup(string vstup)
        {
			bool result = vstup.Any(x => !char.IsLetter(x));
			if(result == false)
			{
				MessageBox.Show("Chyba vstupu! Vstup obsahuje písmena!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
				return false;
			}
			for(int g = 0; g < vstup.Length; g++)
			{
				if (vstup[g] == '/' && g != vstup.Length - 1)
				{
					if(((vstup[g+1] == '+' || vstup[g + 1] == '-') && vstup[g + 2] == '0') || vstup[g + 1] == '0')
					{
						MessageBox.Show("Chyba vstupu! Delenie nulou!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
						return false;
					}
				}
			}
			int zatL = 0;
            int zatP = 0;
            for (int j = 0; j < vstup.Length; j++)
            {
                if (vstup[j] == '+' || vstup[j] == '-')
                {
                    if (j == vstup.Length - 1 && (vstup[j - 1] == '+' || vstup[j - 1] == '-' || vstup[j - 1] == ','))
                    {
                        MessageBox.Show("Chyba vstupu! Zkontrolujte znamenka!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return false;
                    }
                    if (j != vstup.Length - 1 && j != 0 && (vstup[j + 1] == '+' || vstup[j + 1] == '-' || vstup[j + 1] == ','))
                    {
                        MessageBox.Show("Chyba vstupu! Zkontrolujte znamenka!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return false;
                    }
                }
                if (vstup[j] == '(')
                {
                    zatL++;
                }
                if (vstup[j] == ')')
                {
                    zatP++;
                    if (zatP == 1 && zatL == 0)
                    {
                        MessageBox.Show("Chyba vstupu! Zkontrolujte závorky!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        return false;
                    }
                }

            }

            if (zatL != zatP)
            {
                MessageBox.Show("Chyba vstupu! Zkontrolujte závorky!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return false;
            }
            return true;
        }

        /// <summary>
        /// rovná sa =
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button11_Click(object sender, EventArgs e)
        {
            if (textBox1.Text.Length == 1)
            {
                return;
            }
            if (textBox1.Text == "")
            {
                return;
            }
            else
            {
                if (Vstup(textBox1.Text) == false)
                {
                    return;
                }
            }
            string vystup = "";
			string vstup = textBox1.Text;
            if (textBox1.Text.Contains('√'))
            {
                for (int i = 0; i < textBox1.Text.Length; i++)
                {
                    if (textBox1.Text[i] == '√')
                    {
                        if (i == 0)
                        {
                            textBox1.Text = textBox1.Text.Insert(i, "2");
                        }
                        if (i != 0 && char.IsDigit(textBox1.Text[i - 1]) == false)
                        {
                            textBox1.Text = textBox1.Text.Insert(i, "2");
                        }
                    }
                }
            }
            if (textBox1.Text.Contains('(') || textBox1.Text.Contains(')'))
            {
                vystup = spracovanie_zatvorky(textBox1.Text);
            }
            else
            {
                try
                {
                    vystup = math.Zpracovat_Vyraz(textBox1.Text);
                }
                catch
                {
                    MessageBox.Show("Chyba vstupu! Zkontrolujte znaménka, závorky a dělení nulou!", "Chyba!", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }


            }
            if (vystup == "")
            {
                return;
            }
            if (vystup[0] == '+')
            {
                vystup = vystup.Remove(0, 1);
                textBox1.Text = vystup;

			}
            else
            {
                textBox1.Text = vystup;
            }
			listBox1.Items.Add(vstup+"="+vystup);
        }

        /// <summary>
        /// Výpočet tangens zadaného vstupu
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        protected void button14_Click(object sender, EventArgs e)
        {
            if (textBox1.Text.Length == 0)
            {
                return;
            }
            if (textBox1.Text == "")
            {
                return;
            }
            else
            {
                if (Vstup(textBox1.Text) == false)
                {
                    return;
                }
            }
            if (textBox1.Text.Contains('(') && textBox1.Text.Contains(')'))
            {
				double cislo;
				try
				{
					cislo = Convert.ToDouble(spracovanie_zatvorky(textBox1.Text));
				}
				catch
				{
					return;
				}
                try
                {
                    textBox1.Text = Convert.ToString(math.Tangens(cislo));
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Chyba: " + ex.Message, "Chyba", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                return;
            }
            if (textBox1.Text.Contains('/') || textBox1.Text.Contains('*') || textBox1.Text.Contains('+') || textBox1.Text.Contains('-') || textBox1.Text.Contains('^'))
			{
				string text = math.Zpracovat_Vyraz(textBox1.Text);
				double cislo = Convert.ToDouble(text);
				try
				{
					textBox1.Text = Convert.ToString(math.Tangens(cislo));
				}
				catch (Exception ex)
				{
					MessageBox.Show("Chyba: " + ex.Message, "Chyba", MessageBoxButtons.OK, MessageBoxIcon.Error);
					return;
				}
			}
			else
			{
				double cislo = Convert.ToDouble(textBox1.Text);
				try
				{
					textBox1.Text = Convert.ToString(math.Tangens(cislo));
				}
				catch (Exception ex)
				{
					MessageBox.Show("Chyba: " + ex.Message, "Chyba", MessageBoxButtons.OK, MessageBoxIcon.Error);
					return;
				}
			}
		}

		/// <summary>
		/// mazanie jednotlivých znakov
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		protected void button23_Click(object sender, EventArgs e)
		{
			if (textBox1.Text.Length != 0)
			{
				textBox1.Text = textBox1.Text.Remove(textBox1.Text.Length - 1);
			}
		}

		/// <summary>
		/// Spustí help
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		protected void button24_Click(object sender, EventArgs e)
		{
			Form napoveda = new napoveda();
			napoveda.Show();
		}

		/// <summary>
		/// Spusti testy
		/// </summary>
		protected void Spusteni_testu()
		{
			Form testy = new Testy();
			testy.Show();
		}

		/// <summary>
		/// Zapis odmocniny do textbox
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		protected void button13_Click(object sender, EventArgs e)
		{
			textBox1.Text = textBox1.Text + "√";
		}



		/// <summary>
		/// Kontroluje stisknuti Enter, Delete
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		protected void textBox1_KeyDown(object sender, KeyEventArgs e)
		{
			if (e.KeyData == Keys.Enter)
			{
				button11.PerformClick();
				textBox1.SelectionStart = textBox1.Text.Length;
				textBox1.SelectionLength = 0;
			}
			if (e.KeyData == Keys.Delete)
			{
				button22.PerformClick();
			}
			if (e.KeyData == (Keys.Control | Keys.V))
				(sender as TextBox).Paste();
			if (e.KeyData == (Keys.Control | Keys.C))
				(sender as TextBox).Copy();
			if (e.KeyData == (Keys.Control | Keys.A))
				(sender as TextBox).SelectAll();

		}

		

		/// <summary>
		/// Kontroluje jake znaky byly stisknuty, pokud jde o nepovoleny znak, je jeho zapis do textbox zrusen
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		protected void textBox1_KeyPress(object sender, KeyPressEventArgs e)
		{
			
			String sKeys = "1234567890+-*/^(),!\b;";
			if (!sKeys.Contains(e.KeyChar.ToString().ToUpper()))
				e.Handled = true;
		}

		/// <summary>
		/// Faktorial
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		protected void button25_Click(object sender, EventArgs e)
		{
			textBox1.Text = textBox1.Text + "!";
		}

		/// <summary>
		/// výpočet smerodatnej odchylky zo vstupu
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		protected void SO_button_Click(object sender, EventArgs e)
		{
			if (textBox1.TextLength < 1)
			{
				MessageBox.Show("Chyba vstupu!", "Chyba", MessageBoxButtons.OK, MessageBoxIcon.Error);
				return;
			}

			List<double> pole = new List<double>();
			string vstup = textBox1.Text;
			int pocet_cisel = 0;

			string[]tmp = textBox1.Text.Split(';');
			foreach (string x in tmp)
			{
				try
				{
					pole.Add(Convert.ToDouble(x));
				}
				catch (FormatException ex)
				{
					MessageBox.Show("Chyba: "+ex.Message, "Chyba", MessageBoxButtons.OK, MessageBoxIcon.Error);
					return;
				}
				pocet_cisel++;
			}
			try
			{
				textBox1.Text = math.odchylka_s(pocet_cisel, pole).ToString();
			}
			catch(Exception ex)
			{
				MessageBox.Show("Chyba: " + ex.Message, "Chyba", MessageBoxButtons.OK, MessageBoxIcon.Error);
				return;
			}
			

		}
		/// <summary>
		/// vloženie ';' do vstupu
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
        protected void button26_Click(object sender, EventArgs e)
        {
            textBox1.Text = textBox1.Text + ";";
        }

		private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
		{

		}

		/// <summary>
		/// zápis do hystórie
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void listBox1_DoubleClick(object sender, EventArgs e)
		{
			try
			{
				textBox1.Text = listBox1.SelectedItem.ToString().Split('=')[0];
			}
			catch
			{

			}
		}
		/// <summary>
		/// visibilita textboxu histórie
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
		private void button27_Click(object sender, EventArgs e)
		{
			if (listBox1.Visible)
			{
				listBox1.Visible = false;
			}
			else
			{
				listBox1.Visible = true;
			}
		}

		private void pictureBox1_Click(object sender, EventArgs e)
		{

		}
	}

}
