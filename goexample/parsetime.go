package main

import (
    "fmt"
    "time"
)

func main() {
    layout := "2006-01-02 15:04:05"
    timeStr1 := "2022-03-03 14:23:00"
    timeStr2 := "2022-04-03 17:23:00"
    timeStr3 := "2023-03-03"

    time1, err := time.Parse(layout, timeStr1)
    if err != nil {
        fmt.Println("Error parsing time1:", err)
        return
    }

    time2, err := time.Parse(layout, timeStr2)
    if err != nil {
        fmt.Println("Error parsing time2:", err)
        return
    }

    if len(timeStr3) == 10 {
        timeStr3 = timeStr3 + " 00:00:00"
    }
    
    time3,err := time.Parse(layout, timeStr3)
    if err != nil {
        fmt.Println("Error parsing time3:", err)
        return

    }

    if time1.Before(time2) {
        fmt.Println(timeStr1, "is before", timeStr2)
    } else if time1.After(time2) {
        fmt.Println(timeStr1, "is after", timeStr2)
    } else {
        fmt.Println(timeStr1, "is equal to", timeStr2)
    }
    if time3.After(time2) {
        fmt.Println(timeStr3, "is after", timeStr2)
    } else {
        fmt.Println(timeStr3, "is before", timeStr2)
    }
}
