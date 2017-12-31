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

func main() {

	/* Get Option Parser
	 */
	read1 := flag.String("1", "", "Read1")
	read2 := flag.String("2", "", "Read2")
	output := flag.String("o", "", "Output")
	quality := flag.Int("n", 33, "Qualit Score")
	qc_number := byte(*quality)
	flag.Parse()
	/* Generate Output
	 */
	l := 0
	Q20 := 0
	Q30 := 0
	GC := 0
	N := 0
	totalbase := 0
	data1IO, _ := lpp.GetBlockRead(*read1, "\n", false, 10000000)

	OUTPUT, err := os.Create(*output + ".stats")
	data2IO, _ := lpp.GetBlockRead(*read2, "\n", false, 10000000)
	if err != nil {
		panic("Can not Create Result File!!")
	}

	for {

		line, err := data1IO.Next()
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
					fmt.Println(string(line_cont))

				} else if string(line_cont[i]) == "G" || string(line_cont[i]) == "C" {

					GC += 1
				}
			}
		}

	}
	for {

		line, err := data2IO.Next()
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
					fmt.Println(string(line_cont))

				} else if string(line_cont[i]) == "G" || string(line_cont[i]) == "C" {

					GC += 1
				}
			}
		}

	}

	// Result
	BufOUTPUT := bufio.NewWriterSize(OUTPUT, 9999)
	BufOUTPUT.WriteString("TotalBase\tTotalReadsNumber\tQ20%\tQ30%\tN%\tGC%\n")
	BufOUTPUT.WriteString(fmt.Sprintf("%d\t%d\t%.2f\t%.2f\t%.2f\t%.2f\n", totalbase, l/4, 100*float64(Q20)/float64(totalbase), 100*float64(Q30)/float64(totalbase), 100*float64(N)/float64(totalbase), 100*float64(GC)/float64(totalbase)))
	BufOUTPUT.Flush()

}
