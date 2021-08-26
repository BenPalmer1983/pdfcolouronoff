import os


class pdfcoo:

  input_file_name = None
  pdf_in = None
  start = None
  end = None
  colour = []


  def run(input_file_name):
    pdfcoo.input_file_name = input_file_name
    pdfcoo.read()
    pdfcoo.make_pdf()


  def read():
    fh = open(pdfcoo.input_file_name, 'r')
    for line in fh:
      line = line.strip()
      if(line[0:5].upper() == "FILE:"):
        f = line.split(":")
        pdfcoo.pdf_in = f[1].strip()
      elif(line[0:6].upper() == "START:"):
        f = line.split(":")
        pdfcoo.start = int(f[1].strip())
      elif(line[0:4].upper() == "END:"):
        f = line.split(":")
        pdfcoo.end = int(f[1].strip())
      elif(line[0:7].upper() == "COLOUR:"):
        f = line.split(":")
        pages = f[1].split(",")
        for p in pages:
          pdfcoo.colour.append(p.strip())
    fh.close()

  def make_pdf():
    try:
      os.mkdir("temp")
    except:
      pass

    if(pdfcoo.input_file_name == None or pdfcoo.pdf_in == None or pdfcoo.start == None or pdfcoo.end == None):
      print("Check input file")
      exit()


    file_out = pdfcoo.pdf_in.replace('.pdf', '_processed.pdf')
    if(file_out == pdfcoo.pdf_in):
      exit()

    pages = []
    for i in range(pdfcoo.end):
      pages.append("G")

    for pg in pdfcoo.colour:
      if("-" in pg):
        f = pg.split("-")
        pg_start = int(f[0])-1
        pg_end = int(f[1])
        for pg in range(pg_start, pg_end):
          if(pg >= 0 and pg < len(pages)):
            pages[pg] = "C"
      else:
        pg = int(pg) - 1
        if(pg >= 0 and pg < len(pages)):
          pages[pg] = "C"
    
    print_blocks = []

    last_n = pdfcoo.start
    last_v = pages[last_n - 1]
 
    pgn = pdfcoo.start
    while(pgn <= pdfcoo.end):
      if(last_v != pages[pgn - 1]):
        print_blocks.append([last_v, last_n , pgn-1])
        last_n = pgn
        last_v = pages[pgn - 1]     
      elif(pgn == pdfcoo.end):
        print_blocks.append([last_v, last_n , pgn])
      pgn = pgn + 1
    


    files = []
    for n in print_blocks:
      output_file = "temp/page_" + str(n[1]) + "_" + str(n[2]) + "_" + n[0] + ".pdf"
      files.append(output_file)
      if(n[0].upper() == "C"):
        cmd = "gs -sDEVICE=pdfwrite -o " + output_file + " -dFirstPage=" + str(n[1]) + " -dLastPage=" + str(n[2]) + "  " + pdfcoo.pdf_in
        os.system(cmd)
      else:
        cmd = "gs -sDEVICE=pdfwrite -dProcessColorModel=/DeviceGray -dColorConversionStrategy=/Gray -dPDFUseOldCMS=false -o " + output_file + " -dFirstPage=" + str(n[1]) + " -dLastPage=" + str(n[2]) + "  " + pdfcoo.pdf_in
        os.system(cmd)


    cmd = "gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=" + file_out + " -dBATCH"
    for n in files:
      cmd = cmd + " " + n
    os.system(cmd)
    
    for n in files:
      os.remove(n)
    os.rmdir("temp")

    # ["3-5","31","51-52"]

    """
    for i in range(pdfcoo.start, pdfcoo.end+1):
      n= str(i)
      while(len(n)<4):
        n = "0" + n
      output_file = "temp/page_" + n
      cmd = "gs -sDEVICE=pdfwrite -o " + output_file + " -dFirstPage=" + str(i) + " -dLastPage=" + str(i) + "  " + pdfcoo.pdf_in
      os.system(cmd)
    """




pdfcoo.run("input.in")


