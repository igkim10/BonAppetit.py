from bs4 import BeautifulSoup
import requests
import webbrowser
import random
import shutil
import imageio
import matplotlib.pyplot as plt

def print_recipes(main_ingredient) :
    page_num = random.randint(1,5)
    print("Recipes from page number " + str(page_num))
    url = "https://www.bonappetit.com/ingredient/" + main_ingredient +"/page/" + str(page_num)
    web_page = requests.get(url)
    soup = BeautifulSoup(web_page.content, 'html.parser')
    bonappetitLinks = []
    for i in range(1) :
        for link in soup.findAll('a') :
            bonappetitLinks.insert(i,link.get('href'))
    print(len(bonappetitLinks))
    if (len(bonappetitLinks) < 51):
        print("Insufficient Recipes Found, Select Y to try again")
    else:
        bonappetitRecipes = []
        for i in range(32,70, i+2) :
            bonappetitRecipes.insert(i,bonappetitLinks[i])
        for i in range(len(bonappetitRecipes)):
            text = str(bonappetitRecipes[i])
            text = text.split('/')
            title = text[len(text)-1]
            tag = text[len(text)-2]
            title = title.replace('-',' ')
            print("[" + str(i) + "] " + str(title))
        recipe_choice = input("\nwhich recipe do you want to open? ")
        recipe_choice = int(recipe_choice)
        url4 = 'https://bonappetit.com' + bonappetitRecipes[recipe_choice]
        text1 = str(bonappetitRecipes[recipe_choice])
        text1 = text1.split('/')
        title = text1[len(text) - 1]
        title = title.replace('-',' ')
        tag = text1[len(text) - 2]
        if(tag == 'recipe'):
            print("\n" + str(title)+ " recipe \n\n")
            web_page1 = requests.get(url4)
            soup2 = BeautifulSoup(web_page1.content,'html.parser')
            for ul in soup2.findAll('ul', class_ = 'ingredients__group'):
                for text in ul.findAll('li', class_ = 'ingredient') :
                    for text2 in text.findAll('div', class_ = 'ingredients__text') :
                        print(text2.text) 
        
            print("\nSteps:\n")
            for ul in soup2.findAll('ul', class_ = 'steps'):
                for li in ul.findAll('li', class_ = 'step'):
                    print(li.text)
        
            print("\nImage:\n")
            for img in soup2.findAll('img', class_ = 'ba-picture--fit'):
                partiallink = img['srcset']
                filename = partiallink.split('/')[-1]

                r = requests.get(partiallink, stream = True)
                if r.status_code == 200:
                    r.raw.decode_content = True

                    with open(filename,'wb') as f:
                        shutil.copyfileobj(r.raw,f)
                        image = imageio.imread(filename)
                        plt.imshow(image)
                        plt.show()
                    
                else:
                    print("bad")

        else:
            print("\nyou opened a story/slideshow, please wait while we redirect you")
            chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
            webbrowser.get(chrome_path).open(url4)  

    

def recipebook() :
    print("\n\nHi! Welcome to my program. This program helps you decide what to cook from a main ingredient. \n\nIf you don't like the recipe selection the first time, keep entering the main ingredient to find one that you like!")
    print("When entering the main ingredient please use lowercase, keep it to one word, and the singular version of the word. Ex: strawberry, chicken\n\n")
    userChoice = input("enter your main ingredient ")
    print_recipes(userChoice)
    
    response = input("\nWant more? (y/n) ")

    if(response =='y'):
        recipebook()
    elif(response == 'n') :
        print('thanks! \nI hope you enjoyed my program!\nHappy Cooking :)')
        return



def main():
    recipebook()


if __name__ == "__main__":
    main()