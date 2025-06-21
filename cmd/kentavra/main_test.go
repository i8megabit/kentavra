package main

import (
	"os/exec"
	"testing"
)

func TestVersion(t *testing.T) {
	cmd := exec.Command("go", "run", "./main.go", "version")
	out, err := cmd.CombinedOutput()
	if err != nil {
		t.Fatalf("run failed: %v", err)
	}
	if string(out) == "" {
		t.Fatal("no output")
	}
}
