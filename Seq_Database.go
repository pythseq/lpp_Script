// N50
package main

import (
	//	"bufio"
	"bytes"
	"flag"
	"fmt"
	. "lpp"
	"os"
	//	"sort"
	"regexp"
)

func main() {
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
	reg := regexp.MustCompile(`\s+`)
	RESULT, _ := os.Create(*output)

	for {
		line, err := fasta_handle.Next()
		data := bytes.SplitN(line, []byte("\n"), 2)
		seq := data[1]
		title := data[0]
		cache := reg.Split(string(title), 2)
		name := cache[0]
		annotation := cache[1]
		if name[0] == '>' {
			name = name[1:]
		}

		//		name := string(data[0])
		seq = bytes.Replace(seq, []byte("\n"), []byte(""), -1)
		seq_length := len(seq)
		RESULT.WriteString(fmt.Sprintf("%s\t%s\t%d\n", name, annotation, seq_length))

		//		_, ok := length_Ddict[all_length][name]
		//		if !ok {
		//			length_Ddict[all_length] = make(map[string]string)
		//			length_Ddict[all_length][name] = ""
		//		}
		if err != nil {
			break
		}

	}

}
