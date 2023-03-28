package main

import (
	"fmt"
	"os"
	"path/filepath"
	"bufio"
	)

type TestFile struct{
	FileName string
	SearchPath string
	AbsPath string
}

func NewTestFile(fileName string, searchPath string) *TestFile{
	//searchPath是否是一个文件目录
	if info,err := os.Stat(searchPath); err != nil || !info.IsDir(){
		fmt.Println("searchPath is not a directory")
		return nil
	}
	return &TestFile{
		FileName: fileName,
		SearchPath: searchPath,
	}
}

//检查文件是否存在
func (t *TestFile) IsExist() bool{
	err := filepath.Walk(t.SearchPath, func(path string, info os.FileInfo, err error) error {
		//如果遍历目录出现错误，则返回错误信息
		if err != nil {
			return err
		}
		//如果遍历到的是目录，则继续遍历
		if info.IsDir(){
			return nil

		}
		//遍历到目标文件，则返回SkipDir，停止遍历
		if info.Name() == t.FileName{
			t.AbsPath = path
		return filepath.SkipDir
	}
		return nil
	})

	if err != nil {
		fmt.Println(err)
		return false
	}
	return true
}

func (t *TestFile) GetAbsPath() string{
	return t.AbsPath
}

//按行读取文件，返回一个字符串切片
func (t *TestFile) ReadLines() []string{

	file, err := os.Open(t.AbsPath)
	if err != nil {
		fmt.Println(err)
		return nil
	}
	defer file.Close()

	lines := []string{}
	scanner := bufio.NewScanner(file)
	for scanner.Scan(){
		lines = append(lines, scanner.Text())
	}
	if err := scanner.Err(); err != nil {
		fmt.Println(err)
		return nil
	}
	return lines

}


func (t *TestFile) GetTotalRows() int{
	file , err := os.Open(t.AbsPath)
	if err != nil {
		fmt.Println(err)
		return 0
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	totalRows := 0
	for scanner.Scan(){
		totalRows++
	}
	if err := scanner.Err(); err != nil {
		fmt.Println(err)
		return 0
	}
	return totalRows
}
