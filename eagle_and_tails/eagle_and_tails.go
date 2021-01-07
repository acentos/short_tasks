package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"time"
)

func main() {

	var (
		e = bufio.NewScanner(os.Stdin)
		t = bufio.NewScanner(os.Stdin)
		r string
		n int
	)

	fmt.Printf("Enter eagle: %s", e.Text())
	e.Scan()

	fmt.Printf("Enter tails: %s", t.Text())
	t.Scan()

	rand.Seed(time.Now().UnixNano())
	var side1, side2 int = rand.Intn(1000), rand.Intn(1000)

	if side1 > side2 {
		r, n = e.Text(), side1
	} else if side1 < side2 {
		r, n = t.Text(), side2
	} else {
		fmt.Println("try again...")
	}

	fmt.Printf("Result is \"%v\" with rand num = %v.\n", r, n)

}
