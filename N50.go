// N50
package main

import (
	//	"bufio"
	"bytes"
	"flag"
	"fmt"
	. "lpp"
	"os"
	"sort"
)

func main() {
	var all_length int = 0
	//	var length_Ddict map[int]map[string]string = make(map[int]map[string]string)

	file := flag.String("i", "", "input Fasta!")
	output := flag.String("o", "", "Output!")
	flag.Parse()
	if *file == "" {
		os.Exit(1)
	}
	fasta := new(Block_Reading)
	fasta.File = *file
	fasta.Blocktag = "\n>"
	fasta_handle, _ := fasta.Read()
	length_slice := []int{}

	for {
		line, err := fasta_handle.Next()
		data := bytes.SplitN(line, []byte("\n"), 2)
		seq := data[1]
		//		name := string(data[0])
		seq = bytes.Replace(seq, []byte("\n"), []byte(""), -1)
		seq_length := len(seq)

		length_slice = append(length_slice, seq_length)
		all_length = all_length + seq_length
		//		_, ok := length_Ddict[all_length][name]
		//		if !ok {
		//			length_Ddict[all_length] = make(map[string]string)
		//			length_Ddict[all_length][name] = ""
		//		}
		if err != nil {
			break
		}

	}

	sort.Sort(sort.Reverse(sort.IntSlice(length_slice)))
	var N10, N20, N30, N40, N50, N60, N70, N80, N90 int
	var sum_length int = 0

	for _, length := range length_slice {
		sum_length = sum_length + length
		if sum_length >= all_length/10 && N10 == 0 {
			N10 = length

		}
		if sum_length >= all_length/5 && N20 == 0 {
			N20 = length

		}
		if sum_length >= all_length*3/10 && N30 == 0 {
			N30 = length

		}
		if sum_length >= all_length*2/5 && N40 == 0 {
			N40 = length

		}

		if sum_length >= all_length/2 && N50 == 0 {
			N50 = length

		}
		if sum_length >= all_length*3/5 && N60 == 0 {
			N60 = length

		}
		if sum_length >= all_length*7/10 && N70 == 0 {
			N70 = length

		}
		if sum_length >= all_length*4/5 && N80 == 0 {
			N80 = length

		}
		if sum_length >= all_length*9/10 && N90 == 0 {
			N90 = length

		}

	}

	max := length_slice[0]
	min := length_slice[len(length_slice)-1]

	STATOUT, _ := os.Create(*output + ".stats")
	STATOUT.WriteString("N50\tMax\tMin\tSum.Base\n")
	STATOUT.WriteString(fmt.Sprintf("%d\t%d\t%d\t%d\n", N50, max, min, all_length))
	SCOPE, _ := os.Create(*output + ".scope")
	SCOPE.WriteString(fmt.Sprintf("%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n", N10, N20, N30, N40, N50, N60, N70, N80, N90))
}
