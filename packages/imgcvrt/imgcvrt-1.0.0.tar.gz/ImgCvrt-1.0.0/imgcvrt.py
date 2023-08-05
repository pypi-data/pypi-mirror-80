from PIL import Image

class Convert:

	def __init__(self, filename):
		self.img = Image.open(filename)

	def toJpg(self, filename):
		img = self.img.convert("RGB")
		img.save(f"{filename}.jpg", "JPEG")
		print("Successfully")

	def toPng(self, filename):
		img = self.img.convert("RGBA")
		self.img.save(f"{filename}.png", "png")

	def toWebp(self, filename):
		self.img.save(f"{filename}.webp", "WEBP")

	def toPdf(self, filename):
		self.img.save(f"{filename}.pdf", "PDF")

	def toIco(self, filename):
		self.img.save(f"{filename}.ico", "ICO")

	def toBmp(self, filename):
		self.img.save(f"{filename}.bmp", "BMP")

	def toEps(self, filename):
		self.img.save(f"{filename}.eps", "EPS")

	def toGif(self, filename):
		self.img.save(f"{filename}.gif", "GIF")

	def toIcns(self, filename):
		self.img.save(f"{filename}.icns", "ICNS")

	def toIm(self, filename):
		self.img.save(f"{filename}.im", "IM")

	def toMsp(self, filename):
		self.img.save(f"{filename}.msp", "MSP")

	def toPcx(self, filename):
		self.img.save(f"{filename}.pcx", "PCX")

	def toPpm(self, filename):
		self.img.save(f"{filename}.ppm", "PPM")

	def toSgi(self, filename):
		self.img.save(f"{filename}.sgi", "SGI")

	def toSpd(self, filename):
		self.img.save(f"{filename}.spider", "SPIDER")

	def toTga(self, filename):
		self.img.save(f"{filename}.tga", "TGA")

	def toTiff(self, filename):
		self.img.save(f"{filename}.tiff", "TIFF")

	def toDcx(self, filename):
		self.img.save(f"{filename}.dcx", "DCX")

	def toPsd(self, filename):
		self.img.save(f"{filename}.psd", "PSD")



