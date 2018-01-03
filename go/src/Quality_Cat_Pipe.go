// GetSeq
package main

import (
	"bufio"
	"bytes"
	"flag"
	"fmt"
	"lpp"
	"os"
)

func QC(datahandle *os.File, qc_number byte) [6]int {
	l := 0
	Q20 := 0
	Q30 := 0
	GC := 0
	N := 0
	totalbase := 0
	rawIO := datahandle

	dataIO := lpp.GetBlockRead(rawIO, "\n", false, 10000000)
	for {

		line, err := dataIO.Next()
		if err != nil {
			break
		}
		l += 1
		if l%4 == 0 {
			line_cont := bytes.Split(line, []byte("\n"))[0]

			for i := 0; i < len(line_cont); i++ {
				if line_cont[i]-qc_number > 20 {
					Q20 += 1
					if line_cont[i]-qc_number > 30 {
						Q30 += 1
					}
				}

			}
		} else if l%2 == 0 {

			line_cont := bytes.Split(line, []byte("\n"))[0]
			totalbase += len(line_cont)
			for i := 0; i < len(line_cont); i++ {
				if string(line_cont[i]) == "N" {
					N += 1

				} else if string(line_cont[i]) == "G" || string(line_cont[i]) == "C" {

					GC += 1
				}
			}
		}

	}
	return [6]int{l, totalbase, Q20, Q30, GC, N}
}

func main() {

	/* Get Option Parser
	 */

	output := flag.String("o", "", "Output")
	quality := flag.Int("n", 33, "Qualit Score")
	qc_number := byte(*quality)
	flag.Parse()

	l := 0
	Q20 := 0
	Q30 := 0
	GC := 0
	N := 0
	totalbase := 0
	data1 := QC(os.Stdin, qc_number)

	l = data1[0]
	totalbase = data1[1]
	Q20 = data1[2]
	Q30 = data1[3]
	GC = data1[4]
	N = data1[5]
	//	fmt.Println(data1, data2)
	/* Generate Output
	 */
	OUTPUT, err := os.Create(*output + ".stats")

	if err != nil {
		panic("Can not Create Result File!!")
	}

	BufOUTPUT := bufio.NewWriterSize(OUTPUT, 9999)
	BufOUTPUT.WriteString("TotalBase\tTotalReadsNumber\tQ20%\tQ30%\tN%\tGC%\n")
	BufOUTPUT.WriteString(fmt.Sprintf("%d\t%d\t%.2f\t%.2f\t%.2f\t%.2f\n", totalbase, l/4, 100*float64(Q20)/float64(totalbase), 100*float64(Q30)/float64(totalbase), 100*float64(N)/float64(totalbase), 100*float64(GC)/float64(totalbase)))
	BufOUTPUT.Flush()

}
