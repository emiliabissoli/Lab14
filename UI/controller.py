import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def handleCreaGrafo(self, e):

        if self._view._txtIntK == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire il numero di giorni massimo", color="red"))
            self._view.update_page()
            return

        if self._view._ddStore.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare uno store", color="red"))
            self._view.update_page()
            return

        maxK = self._view._txtIntK.value
        try:
            intK = int(maxK)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, inserire un numero", color="red"))
            self._view.update_page()
            return

        store = self._view._ddStore.value
        self._view.txt_result.clean()
        self._model.buildGraph(store,intK)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato: "))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}\nNumero di archi: {self._model.getNumArchi()}"))

        allNodes = self._model.getAllNodes()
        self.fillDDNode(allNodes)

        self._view.update_page()


    def handleCerca(self, e):
        if self._view._ddNode.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare un nodo", color="red"))
            self._view.update_page()
            return

        camminoMassimo = self._model.camminoMassimo(self._view._ddNode.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza : {self._view._ddNode.value}"))
        for n in camminoMassimo:
            self._view.txt_result.controls.append(ft.Text(n))
        self._view.update_page()


    def handleRicorsione(self, e):
        if self._view._ddNode.value is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Attenzione, selezionare un nodo", color="red"))
            self._view.update_page()
            return

        bestpath, bestscore = self._model.getBestPath(self._view._ddNode.value)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Trovato un cammino che parte da {self._view._ddNode.value} "
                    f"con somma dei pesi uguale a {bestscore}."))

        print(bestpath)
        for v in bestpath:
            self._view.txt_result.controls.append(ft.Text(f"{v}"))
        self._view.update_page()


    def fillDDStore(self):
        for s in self._model.getAllStore():
            self._view._ddStore.options.append(ft.dropdown.Option(s))
        self._view.update_page()

    def fillDDNode(self, allNodes):
        self._view._ddNode.options.clear()
        for n in allNodes:
            self._view._ddNode.options.append(
                ft.dropdown.Option(n))

