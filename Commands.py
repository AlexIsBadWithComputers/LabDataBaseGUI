MoCom = ("INSERT INTO MoTable (FilePath, V96, R9295, R9495, R9695, R9795, R9895, R10095, R9195) VALUES "
						"(%s, %s, %s, %s, %s, %s, %s, %s, %s)" )

MoECom =  ("INSERT INTO MoError (FilePath, EV96, E9295, E9495, E9695, E9795, E9895, E10095, E9195) VALUES "
						"(%s, %s, %s, %s, %s, %s, %s, %s, %s)" )

BCom = ("INSERT INTO BTable (FilePath, V11, R1011) VALUES "
						"(%s, %s, %s)" )

BECom = ("INSERT INTO BError (FilePath, EV11, E1011) VALUES "
						"(%s, %s, %s)" )

CuCom = ("INSERT INTO CuTable (FilePath, V63, V65, R6564, R6260, R6160) VALUES "
						"(%s, %s, %s, %s, %s, %s)" )

CuECom = ("INSERT INTO CuError (FilePath, EV63, EV65, E6564, E6260, E6160) VALUES "
						"(%s, %s, %s, %s, %s, %s)" )

UCom = ("INSERT INTO UTable (FilePath, V234, V235, V238,  R234238, R235238) VALUES "
						"(%s, %s, %s, %s, %s, %s)" )
UECom = ("INSERT INTO UError (FilePath, EV234, EV235, EV238, E234238, E235238) VALUES "
						"(%s, %s, %s, %s, %s, %s)" )

FeCom = ("INSERT INTO FeTable (FilePath, RX57, R5754, R5854, RX54) VALUES "
						"(%s, %s, %s, %s, %s)" )

FeECom = ("INSERT INTO FeError (FilePath, EX57, E5754, E5854, EX54) VALUES "
						"(%s, %s, %s, %s, %s)" )

SrCom = ("INSERT INTO SrTable (FilePath, V87, R8786, R8486, R8586) VALUES "
						"(%s, %s, %s, %s, %s)" )

SrECom = ("INSERT INTO SrError (FilePath, EV87, E8786, E8486, E8586) VALUES "
						"(%s, %s, %s, %s, %s)" )

SCom = ("INSERT INTO STable (FilePath, V32, V34, R3234) VALUES "
						"(%s, %s, %s, %s)" )

SECom = ("INSERT INTO SError (FilePath, E32, E34, E3234) VALUES "
						"(%s, %s, %s, %s)" )

ZnCom = ("INSERT INTO ZnTable (FilePath, V66, R6866, R7064, R6864, R6764, R6664, R6768) VALUES "
						"(%s, %s, %s, %s, %s, %s, %s, %s)" )


ZnECom = ("INSERT INTO ZnError (FilePath, EV66, E6866, E7064, E6864, E6764, E6664, E6768) VALUES "
						"(%s, %s, %s, %s, %s, %s, %s, %s)" )


DataCommands = {'Mo':MoCom,'B':BCom,'Cu':CuCom,'U':UCom,'Fe':FeCom,'Sr':SrCom,'S':SCom, 'Zn':ZnCom}
ErrorCommands = {'Mo':MoECom, 'B':BECom, 'Cu':CuECom, 'U':UECom, 'Fe':FeECom, 'Sr':SrECom, 'S':SECom, 'Zn':ZnECom}