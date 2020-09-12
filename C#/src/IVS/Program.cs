using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace IVS
{
	/// <summary>
	/// Hlavni vstupni bod aplikace
	/// </summary>
	static class Program
	{
		/// <summary>
		/// Hlavní vstupní bod aplikace.
		/// </summary>
		[STAThread]
		static void Main()
		{
			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);
			Application.Run(new Calculator());
		}
	}
}
