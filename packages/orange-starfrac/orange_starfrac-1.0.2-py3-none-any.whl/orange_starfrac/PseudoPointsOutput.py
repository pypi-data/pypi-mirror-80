
import Orange.data
from Orange.widgets.widget import OWWidget, Input, Output
from Orange.widgets.utils.widgetpreview import WidgetPreview
from Orange.widgets import gui
from Orange.data import Domain, ContinuousVariable, StringVariable

from orange_starfrac.RpcClient import RpcClient
from orange_starfrac.InputMixin import InputMixin
from orange_starfrac.utils import rowToDict, tableToDictionary

def targetDictionaryFromTable(table):
    dict = {}
    dict["columns"] = []
    dict["metas"] = []
    data = []

    if len(table.domain.metas) == 1:
        dict["metas"].append(table.domain.metas[0].name)
        for row in table:
            res = {}
            res[table.domain.metas[0].name] = row.metas[0]
            data.append(res)

    if len(table.domain.attributes) == 1:
        name = table.domain.attributes[0].name
        dict["metas"].append(name)
        for row in table:
            res = {}
            index = table.domain.index(name)
            res[name] = row[index].value
            data.append(res)

    dict["data"] = data
    return dict

class PseudoPointsOutput(OWWidget, RpcClient, InputMixin):
    name = "Prediction Output"
    description = "Send prediction result data to StarFrac application"
    icon = "icons/mvaPointsOutput.svg"
    priority = 100
    want_main_area = False

    class Inputs:
        data = Input("Data model table", Orange.data.Table, default=True)


    def __init__(self):
        OWWidget.__init__(self)
        RpcClient.__init__(self)
        box = gui.widgetBox(self.controlArea, "Info")
        self.infoa = gui.widgetLabel(box, "No data on input yet, waiting to get something.")
        self.infob = gui.widgetLabel(box, "")

    @Inputs.data
    def set_data(self, dataset):
        if dataset is not None:
            self.infoa.setText("%d instances in input data set" % len(dataset))
            res = targetDictionaryFromTable(dataset)
            if len(res['metas']) == 0:
                self.warning("Can't find column with target variable")
            else:
                self.requestData("setPseudoPointsPrediction", self.dataReceived, res)
        else:
            self.infoa.setText("No data on input yet, waiting to get something.")

    def dataReceived(self, data):
        text = '\n'.join(data)
        self.infoa.setText(text)
        if len(data) > 0:
            self.warning(text)
        else:
            self.warning()
        




if __name__ == "__main__":
    WidgetPreview(PseudoPointsOutput).run()
