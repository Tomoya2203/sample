import pypdf

lis = ["ここに結合したpdfファイルのパス名を入力", "ここに結合したpdfファイルのパス名を入力"]
merger = pypdf.PdfWriter()
for pdf in lis:
    merger.append(pdf)
merger.write("test2.pdf")
merger.close()