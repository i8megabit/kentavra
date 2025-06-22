package main

import (
	"fmt"
	"os"
)

var Version = "2.0.3"

func printHelp() {
	fmt.Println("Kentavra CLI")
	fmt.Println("Usage: kentavra [command]")
	fmt.Println("Commands:")
	fmt.Println("  start   Start services")
	fmt.Println("  stop    Stop services")
	fmt.Println("  status  Show status")
	fmt.Println("  version Show version")
}

func main() {
	if len(os.Args) < 2 {
		printHelp()
		return
	}
	switch os.Args[1] {
	case "start":
		fmt.Println("Starting services (not implemented)")
	case "stop":
		fmt.Println("Stopping services (not implemented)")
	case "status":
		fmt.Println("Status: (not implemented)")
	case "version":
		fmt.Println("Kentavra version", Version)
	case "help":
		printHelp()
	default:
		printHelp()
	}
}
