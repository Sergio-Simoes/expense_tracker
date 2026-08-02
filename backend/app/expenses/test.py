from typing import List
class Solution:
    def removeDuplicates(self, nums: List[int]):
        if nums is None:
            return 0
        new_list=[]
        [new_list.append(i) for i in nums if i not in new_list]

        return new_list
    
    def romanToInt(self, s: str) -> int:
        roman = {   "I" : 1, 
                    "V" : 5,
                    "X" : 10,
                    "L" : 50,
                    "C" : 100,
                    "D" : 500,
                    "M" : 1000 }
                    
        count = 0
        temp= ''
        fstTime=True


        for i in s:
            if not fstTime and temp < roman[i]:
                count -= temp
                count += roman[i] - temp
            else:
                count += roman[i]
                fstTime = False
            
            temp = roman[i]
        
        return count



if __name__ == "__main__":
    sol = Solution()
    # print(sol.removeDuplicates([1,1,2]))
    # print(sol.removeDuplicates([1,1,2,2,2,3]))
    # print(sol.removeDuplicates([1,2,3,4,4]))
    print(sol.romanToInt("IV"))




                