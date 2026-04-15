import json


class guy:
    def __init__(self):
        self.posilki = []
        self.posilki_typ = []

    def get_makro(self):
        self.kcal = int(input("Enter calories: "))
        self.protein = int(input("Enter protein: "))
        self.fat = int(input("Enter fat: "))
        self.carbs = int(input("Enter carbs: "))
        self.target_kcal = self.kcal
        self.target_protein = self.protein
        self.target_fat = self.fat
        self.target_carbs = self.carbs

    def get_score(self, kcal, protein, fat, carbs, recipe):
        score = 0
        score += 1 - abs(kcal - recipe["kcal"]) / kcal
        score += 1 - abs(protein - recipe["bialko"]) / protein
        score += 1 - abs(fat - recipe["tluszcze"]) / fat
        score += 1 - abs(carbs - recipe["weglowodany"]) / carbs
        return score

    def get_score_more_algo(self, kcal, protein, fat, carbs, recipe):
        kcal_error = abs(kcal - recipe["kcal"]) / max(kcal, 1)
        protein_error = abs(protein - recipe["bialko"]) / max(protein, 1)
        fat_error = abs(fat - recipe["tluszcze"]) / max(fat, 1)
        carbs_error = abs(carbs - recipe["weglowodany"]) / max(carbs, 1)

        penalty = kcal_error + protein_error + fat_error + carbs_error

        return 1 - penalty

    def get_current_best(self, recipies, kcal, protein, fat, carbs):
        best = None
        best_score = 0
        for recipe in recipies:
            if recipe["typ"] not in self.posilki_typ:
                recipe_score = self.get_score_more_algo(
                    kcal, protein, fat, carbs, recipe
                )
                if best is None or recipe_score > best_score:
                    best = recipe
                    best_score = recipe_score
        if best is not None:
            return best

        for recipe in recipies:
            if recipe["typ"] not in self.posilki_typ:
                recipe_score = self.get_score_more_algo(
                    kcal, protein, fat, carbs, recipe
                )
                if best is None or recipe_score > best_score:
                    best = recipe
                    best_score = recipe_score
        return best

    def add_posilek(self, posilek):
        self.posilki.append(posilek)
        self.posilki_typ.append(posilek["typ"])
        self.kcal -= posilek["kcal"]
        self.protein -= posilek["bialko"]
        self.fat -= posilek["tluszcze"]
        self.carbs -= posilek["weglowodany"]

    def give_answear(self):
        self.get_makro()
        for i in range(3):
            best = self.get_current_best(
                recipies, self.kcal, self.protein, self.fat, self.carbs
            )
            if best is not None:
                self.add_posilek(best)
            else:
                print("No more recipes available.")
                break
        print("Your meals:")
        for posilek in self.posilki:
            print(posilek)

        actual_kcal = self.target_kcal - self.kcal
        actual_protein = self.target_protein - self.protein
        actual_fat = self.target_fat - self.fat
        actual_carbs = self.target_carbs - self.carbs

        print("\nMacro summary:")
        print(f"Kcal: target {self.target_kcal}, actual {actual_kcal}")
        print(f"Protein: target {self.target_protein}, actual {actual_protein}")
        print(f"Fat: target {self.target_fat}, actual {actual_fat}")
        print(f"Carbs: target {self.target_carbs}, actual {actual_carbs}")


recipies = json.load(open("przepisy.json", "r")).get("przepisy")
user = guy()
user.give_answear()
