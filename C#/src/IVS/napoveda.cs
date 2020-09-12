using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace IVS
{
	/// <summary>
	/// Trida formulare napovedy
	/// </summary>
	public partial class napoveda : Form
	{
		/// <summary>
		/// Init komponent
		/// </summary>
		public napoveda()
		{
			InitializeComponent();
		}

      
		/// <summary>
		/// zavre formular
		/// </summary>
		/// <param name="sender"></param>
		/// <param name="e"></param>
        private void button1_Click(object sender, EventArgs e)
        {
            Close();
        }
    }
}
