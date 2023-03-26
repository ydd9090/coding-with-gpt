package main

import (
	"fmt"
)

type Item struct{
	Status string
}

var Items = []Item {{Status: "open"}, {Status: "closed"}, {Status: "open"}, {Status:"closed"},{Status:"open"},{Status:"closed"},{Status:"open"},{Status:"未知"},{Status:"block"}}

type ItemStatusCount struct {
	Status string
	Count int
}
//遍历Items统计出有多少种状态，并对所有状态计数
func main() {
	var statusMap = make(map[string]int)
	for _, item := range Items {
		statusMap[item.Status]++
	}
	for status, count := range statusMap {
		fmt.Printf("%s: %d ", status, count)
	}
	fmt.Println()
	//遍历statusMap，将结果放入ItemStatusCount数组中
	var statusCount []ItemStatusCount
	for status, count := range statusMap {
		statusCount = append(statusCount, ItemStatusCount{Status: status, Count: count})
	}
	for _, item := range statusCount {
		fmt.Printf("%s: %d", item.Status, item.Count)
	}
	
}