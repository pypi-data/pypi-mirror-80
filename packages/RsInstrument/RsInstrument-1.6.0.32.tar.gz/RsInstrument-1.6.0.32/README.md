RsInstrument module provides convenient way of communicating with R&S instruments.

Check out the full documentation here: https://rsinstrument.readthedocs.io/en/latest/index.html

Version history:

	Version 1.6.0.32 (21.09.2020)
		- Added documentation on readthedocs.org
		- Code changes only relevant for the auto-generated drivers

	Version 1.5.0.30 (17.09.2020)
		- Added recognition of RsVisa library location for linux when using options string 'SelectVisa=rs'
		- Fixed bug in reading binary data 16 bit

	Version 1.4.0.29 (04.09.2020)
		- Fixed error for instruments that do not support \*OPT? query

	Version 1.3.0.28 (18.08.2020)
		- Implemented SocketIO plugin which allows the remote-control without any VISA installation
		- Implemented finding resources as a static method of the RsInstrument class

	Version 1.2.0.25 (03.08.2020)
		- Fixed reading of long strings for NRP-Zxx sessions

	Version 1.1.0.24 (16.06.2020)
		- Fixed simulation mode switching
		- Added Repeated capability

	Version 1.0.0.21
		- First released version