# Perform more advanced analytics to detect and visualize anomalies in the data

In the [previous step](./rules.md) you performed simple analytics and created an alert on the data using IoT Central rules.

In this step, you will perform more advanced analytics to detect and visualize anomalies in the data.

## Anomaly detection

Anomaly detection is the detection of data points in a stream that are unexpected. These can indicate that something is wrong with whatever is being monitored. For example, spikes in vibration when monitoring a machine might mean that a part is wearing out and needs to be replaced.

Anomaly detection can be done using Machine Learning models - models that have been trained to take a stream of data and identify data points that are outside the expected data trend.

In this part you will be detecting anomalies in the sound data to identify unexpected loud noises using spike detection.

> In this project the telemetry values are being monitored every minute, so would only be able to detect a sustained loud noise. In real world scenarios you might want to monitor noise more often to detect spikes. You can also run these tools 'on the edge', that is take the setup in Azure and deploy it to a computer on the same local network as your sensors to make detection faster and cheaper. You can read more about this in the [Azure Stream Analytics on IoT Edge documentation](https://docs.microsoft.com/azure/stream-analytics/stream-analytics-edge?WT.mc_id=academic-7372-jabenn).

### Anomaly detection tools

Microsoft Azure has a couple of anomaly detection tools that can be used.

* [Anomaly detection cognitive service](https://azure.microsoft.com/services/cognitive-services/anomaly-detector/?WT.mc_id=academic-7372-jabenn) - Azure cognitive services are pre-built AI services that you can use from your code. There are a number of services covering speech, vision, language, decision and search, and one of the decision services is the Anomaly detector.
* [Anomaly detection in Stream Analytics](https://docs.microsoft.com/azure/stream-analytics/stream-analytics-machine-learning-anomaly-detection?WT.mc_id=academic-7372-jabenn) - [Azure Stream Analytics](https://azure.microsoft.com/services/stream-analytics/?WT.mc_id=academic-7372-jabenn) is an analytics service that can run real-time queries on live streams of data. This service can query for anomalies.

In this part, you will be using Stream Analytics to query for anomalies from a stream of data from IoT Central. You can learn more about this from the [Real-Time ML Based Anomaly Detection In Azure Stream Analytics episode of the Internet of Things show on Channel9](https://channel9.msdn.com/Shows/Internet-of-Things-Show/Real-Time-ML-Based-Anomaly-Detection-In-Azure-Stream-Analytics?WT.mc_id=academic-7372-jabenn)

[![IoT Show banner](../images/iot-show-stream-analytics-anomaly-detection.png)](https://channel9.msdn.com/Shows/Internet-of-Things-Show/Real-Time-ML-Based-Anomaly-Detection-In-Azure-Stream-Analytics?WT.mc_id=academic-7372-jabenn)

> If you have some experience with cloud services and are able to program using .NET, there is a hands-on learning path on Microsoft Learn that covers a similar scenarios to this part, and shows how to output the data to PowerBI for visualization:
>
> [Identify anomalies by routing data via IoT Hub to a built-in ML model in Azure Stream Analytics](https://docs.microsoft.com/learn/modules/data-anomaly-detection-using-azure-iot-hub/?WT.mc_id=academic-7372-jabenn)

## Set up data in and out

Azure Stream Analytics takes a stream of data from one place, runs a real-time query, then sends the results out as a stream to somewhere else - either another streaming service, or storage. In this lab, data will come from Azure IoT Central, and the results are saved in [Azure Cosmos DB](https://azure.microsoft.com/services/cosmos-db/?WT.mc_id=academic-7372-jabenn), a NoSQL database.

To create and manage the services needed for this step, you will need to be able to navigate the Azure Portal. You can learn more about the portal and how to navigate it in the [Azure Portal overview documentation](https://docs.microsoft.com/azure/azure-portal/azure-portal-overview?WT.mc_id=academic-7372-jabenn).

### Create an event hub

IoT Central by itself cannot send data to other services. Instead you need to set up a data export to another service. The service that you will be sending data to is called [Azure Event Hubs](https://azure.microsoft.com/services/event-hubs/?WT.mc_id=academic-7372-jabenn), which is a fully managed, real-time data ingestion service that can handle millions of events per second from a variety of sources.

To create an Event Hub, you start by creating an Event Hubs namespace, and inside this you create one or more Event Hubs. You can create these using either the [Azure Portal](https://portal.azure.com/?WT.mc_id=academic-7372-jabenn) or the [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli?WT.mc_id=academic-7372-jabenn). The portal is a web UI where you can configure Azure services, the CLI is a command-line tool for creating and managing Azure services.

* If you want to create an Event Hub using the Azure Portal, follow the instructions in [the Create an Event Hub with the Azure Portal quickstart](https://docs.microsoft.com/azure/event-hubs/event-hubs-create?WT.mc_id=academic-7372-jabenn)

* If you want to create an Event Hub using the Azure CLI, follow the instructions in [the Create an Event Hub with the Azure CLI quickstart](https://docs.microsoft.com/azure/event-hubs/event-hubs-quickstart-cli?WT.mc_id=academic-7372-jabenn)

Whichever method you use:

* Name your Resource Group `EnvironmentMonitor`. Resource groups are logical groupings of resources, allowing you to manage them in bulk. For example, when you are done with this lab you will be able to delete this resource group and have that automatically delete all the services in it that you have created.

* The Event Hubs namespace has to be globally unique, so use `environmentmonitor-` followed by something unique, such as your name or the current date

* Make sure the location you chose is the one closest to you

* Use the basic pricing tier. This Event Hubs Namespace won't be handling much data, so the basic tier is more than enough and the cheapest option. You can read more on pricing in the [Event Hubs Pricing guide](https://azure.microsoft.com/pricing/details/event-hubs/?WT.mc_id=academic-7372-jabenn).

* Name your Event Hub `environmentmonitor`

### Create an Event Hub connection string

Once the Event Hub is created, you will need a connection string to be able to connect to it from IoT Central - a key that contains details about the event hub and the permissions. Connection strings are created with different access policies - limits on what can be done when connecting to the Event Hub. To send data, a connection string needs to be created that provides write access.

1. From the Event Hubs namespace in IoT Central, select *Entities -> Event Hubs* from the side menu

    ![The event hubs menu](../images/event-hubs-hubs-menu.png)

1. Select the *environmentmonitor* event hub

    ![The even hubs list](../images/event-hubs-hubs-menu-select-hub.png)

1. Select *Setting -> Shared Access Policies* from the event hub menu

    ![The shared access policies menu](../images/event-hubs-hub-shared-access-policies-menu.png)

1. Select the **+ Add** button

    ![The add button](../images/event-hubs-hub-shared-access-policies-add-button.png)

1. Configure the policy:

    1. Name the policy `IoTCentralExport`
    1. Check the `Send` permission.

1. Select the **Create** button to create the policy

    ![The add policy pane](../images/event-hubs-hub-shared-access-policies-add-dialog.png)

1. Once the policy is created it will appear in the list. Select it.

    ![The policy list](../images/event-hubs-hub-shared-access-policies-list-iot-central.png)

1. Use the copy button to copy the *Connection string-primary key*

    ![The policy details](../images/event-hubs-hub-shared-access-policies-details-iot-central.png)

### Set up IoT Central data export

Once the event hub is created, IoT Central needs to be connected to it. Data export is configured by creating destinations that the data is exported to, and setting up exports to those destinations.

This data can be enriched with properties or custom values. You can read more about how you can configure the data being exported in the [Export IoT data to cloud destinations using data export documentation](https://docs.microsoft.com/azure/iot-central/core/howto-use-data-export?WT.mc_id=academic-7372-jabenn).

#### Create the destination

1. From your IoT Central app, select the **Data Export** tab from the side bar menu (not **Data Export (Legacy)**).

    ![The data export menu](../../../images/iot-central-menu-data-export.png)

1. Select the **Destinations** tab

    ![The destinations tab](../images/iot-central-data-export-destinations-tab.png)

1. Select the **+ New destination** button

    ![The new destination button](../images/iot-central-data-export-destinations-new-destination-button.png)

1. Configure the destination:

    1. Set the *Name* for the destination to `Environment Monitor Event hub`
    1. Set the *Destination Type* to be `Azure Event Hubs`
    1. Paste the connection string you copied earlier from the Event Hub policy into the *Connection string* box

1. Select the **Save** button

    ![The save button](../images/iot-central-data-export-destinations-new-destination-details.png)

#### Create the export

1. From your IoT Central app, select the **Data Export** tab from the side bar menu.

    ![The data export menu](../../../images/iot-central-menu-data-export.png)

1. Select the **Exports** tab

    ![The exports tab](../images/iot-central-data-export-exports-tab.png)

1. Select the **+ New export** button

    ![The new export button](../images/iot-central-data-export-exports-new-export-button.png)

1. Configure the export:

    1. Set the *Name* for the export to `Environment Monitor Event hub`
    1. In the *Data* section, make sure the *Type of data to export* is set to `Telemetry`
    1. In the *Destinations* section, select the **+ Destination** button and select the `Environment Monitor Event hub` destination

1. Select the **Save** button

    ![The save button](../images/iot-central-data-export-exports-new-export-details.png)

The export job will be saved and then started it. It can take a couple of minutes for the job to begin, and you can see the progress from the *Exports* tab.

![The exports list](../images/iot-central-data-export-exports-tab-job-starting.png)

### Create storage for anomalies in Cosmos DB

Azure Cosmos DB is a fast, NoSQL database that can support a wide variety of different APIs from SQL, to MongoDB, to Cassandra. It mixes power and performance, with global replication, and can be connected to services like Stream Analytics.

1. Head to the [Create Azure Cosmos DB Account in the Azure Portal](https://ms.portal.azure.com/?WT.mc_id=academic-7372-jabenn#create/Microsoft.DocumentDB)

1. Configure the Cosmos DB account:

    1. Select you Azure subscription

    1. Use the same Resource Group that you used for the Event Hubs namespace, `EnvironmentMonitor`

    1. The Cosmos DB account name has to be globally unique, so use `environmentmonitor-` followed by something unique, such as your name or the current date

    1. Use the `Core (SQL)` API

    1. Set *Notebooks* to `On`

    1. Make sure the location you chose is the one closest to you

    1. Ensure the *Apply free tier discount* is set to `Apply`

    1. Leave the rest of the values as the defaults

    ![The Cosmos DB account details](../images/cosmos-db-account-details.png)

1. Select the **Review + Create** button

1. Once the details have been validated, select the **Create** button

> It can take up to 15 minutes to create a Cosmos DB account, so leave it creating whilst you do the next steps.

## Set up Stream Analytics

To set up a Stream Analytics job, you need to create the resource, connect the inputs and outputs, and write the query.

### Create the Stream Analytics job

The best place to create a Stream Analytics job is via the [Azure Portal](https://portal.azure.com/?WT.mc_id=academic-7372-jabenn) as it provides a great environment to configure the inputs, outputs and query.

Follow the instructions in [the Create a Stream Analytics job with the Azure Portal documentation](https://docs.microsoft.com/azure/stream-analytics/stream-analytics-quick-create-portal?WT.mc_id=academic-7372-jabenn#create-a-stream-analytics-job). Just do the *Create a Stream Analytics job* section, not the following sections.

* Use the same Resource Group that you used for the Event Hubs namespace, `EnvironmentMonitor`

* Name your Stream Analytics job `AnomalyDetection`

* Make sure the location you chose is the one closest to you

### Set up the input

Once your job has been created, set the Event Hub as the input. Stream Analytics inputs are streams of data that are processed by the job.

1. From the menu, select *Job topology -> Inputs*

    ![The inputs option](../images/stream-analytics-job-topology-inputs.png)

1. Drop down the **+ Add stream input** box and select **Event hub**

    ![The add event hub option](../images/stream-analytics-inputs-add-event-hub.png)

1. Fill in the input details:

    1. Name the input `IoTCentral`

    1. Make sure `Select Event Hub from your subscriptions` is selected

    1. Select your Azure subscription

    1. Select your new Event Hubs namespace

    1. Make sure *Event Hub name* is set to `Use existing`, and select the `environmentmonitor` event hub

    1. Leave the rest of the values as the defaults

1. Select the **Save** button

    ![The event hub details](../images/stream-analytics-inputs-event-hub-details.png)

After a few seconds, the new input will appear.

### Set up the output

Once data has been processed by a Stream Analytics job, the results need to go somewhere, defined by an output.

1. From the menu, select *Job topology -> Outputs*

    ![The outputs option](../images/stream-analytics-job-topology-outputs.png)

1. Drop down the **+ Add** box and select **Cosmos DB**

    ![The add cosmos db option](../images/stream-analytics-outputs-add-cosmos-db.png)

1. Fill in the output details:

    1. Name the output `Anomalies`

    1. Make sure `Select Cosmos DB from your subscriptions` is selected

    1. Select your Azure subscription

    1. Select your new Cosmos DB account

    1. Set the *Database* option to `Create new`

    1. Name the database `EnvironmentMonitor`

    1. Name the collection `Anomalies`

1. Select the **Save** button

    ![The cosmos db details](../images/stream-analytics-outputs-cosmos-db-details.png)

After a few seconds, the new output will appear.

### Write the query

Stream Analytics jobs query data using a SQL-like language.

> You can also add additional features to this language using user defined functions written in JavaScript, C# or via Azure Machine Learning Studio. You can read more about this in the [User-defined functions in Azure Stream Analytics documentation](https://docs.microsoft.com/azure/stream-analytics/functions-overview?WT.mc_id=academic-7372-jabenn#create-a-stream-analytics-job).

1. From the menu, select *Job topology -> Query*

    ![The query option](../images/stream-analytics-job-topology-query.png)

1. The Query Editor will open, and show a preview of the input data from the *IoTCentral* input

    ![The default query](../images/stream-analytics-query-blank.png)

1. The side bar shows the input and outputs that have been defined, the main panel has the query above, and a results panel blow that can show a preview of the input, or the results of the query. When you write a query you can test it, and see the sample results without them being sent to the output - nothing is sent to the output until you save and start the job.

1. Use the following code for the query:

    ```sql
    WITH AnomalyDetectionStep AS
    (
        SELECT
            EVENTENQUEUEDUTCTIME AS time,
            deviceId as device_id,
            CAST(telemetry.sound AS float) AS sound_level,
            AnomalyDetection_SpikeAndDip(CAST(telemetry.sound AS float), 95, 120, 'spikes')
                OVER(PARTITION BY deviceId LIMIT DURATION(second, 600)) AS spike_scores
        FROM
            [IoTCentral]
    )
    SELECT
        time,
        device_id,
        sound_level,
        CAST(GetRecordPropertyValue(spike_scores, 'Score') AS float) AS spike_score,
        CAST(GetRecordPropertyValue(spike_scores, 'IsAnomaly') AS bigint) AS is_spike_anomaly
    INTO
        [Anomalies]
    FROM
        AnomalyDetectionStep
    ```

    This query uses the `AnomalyDetection_SpikeAndDip` function to detect spikes in the data. It looks over the last 600 seconds (10 minutes) and detects spikes with a 95% confidence (Machine Learning models rarely return true or false values, instead they return probabilities). The data is partitioned by the `deviceId`, meaning that it looks for spikes on a per-device basis, rather than spikes across all devices. This is to avoid spikes when the background audio level of one device is different to another.

    You can read more on this function in the [AnomalyDetection_SpikeAndDip documentation](https://docs.microsoft.com/stream-analytics-query/anomalydetection-spikeanddip-azure-stream-analytics?WT.mc_id=academic-7372-jabenn).

1. Test the query using the **Test Query** button. Before you run the test, create some spikes using loud noises, verifying the spikes using the IoT Central device view.

    ![The test query button](../images/stream-analytics-query-test-button.png)

    If there was any spikes in the sound levels, you will see the value marked with a `1` in the *is_spike_anomaly* column.

    | time                           | sound_level | device_id              |spike_score         | is_spike_anomaly |
    | ------------------------------ | ----------- | ---------------------- | ------------------- | ---------------- |
    | "2020-08-22T19:52:03.1410000Z" | 82          | pi-environment-monitor | 0.083631182941302   | 0                |
    | "2020-08-22T19:51:52.3420000Z" | 82          | pi-environment-monitor | 0.08810036827344042 | 0                |
    | "2020-08-22T19:51:42.3230000Z" | 109         | pi-environment-monitor | 0.0262244803744075  | 1                |
    | "2020-08-22T19:51:31.9150000Z" | 80          | pi-environment-monitor | 0.10735258744061232 | 0                |
    | "2020-08-22T19:51:20.5050000Z" | 80          | pi-environment-monitor | 0.11193847268271984 | 0                |

    Due to the random nature of the simulated device, it will show a lot of spikes.

1. Save the query by selecting the **Save query** button

    ![The save query button](../images/stream-analytics-query-save-query-button.png)

1. Head to the Stream Analytics Job *Overview*

    ![The overview menu](../images/stream-analytics-overview.png)

1. Select the **Start** button

    ![The start button](../images/stream-analytics-overview-start-button.png)

1. Make sure the *Job output start time* is set to `Now` and select the **Start** button to start the job

    ![The start dialog](../images/stream-analytics-overview-start-dialog.png)

The job *status* will change to `Starting`.After a few minutes the job will start up and send the output to Cosmos DB. You will get a notification when the job has started, and the *status* will change to `Running`

## Test the anomaly detection

You can test the output by viewing the data in Cosmos DB.

### View the raw data

1. Navigate to your Cosmos DB account

1. Select **Data Explorer**

    ![The data explorer menu](../images/cosmos-db-data-explorer-menu.png)

1. You can view the raw data by expanding the *EnvironmentMonitor* in the **DATA** section, then expanding *Anomalies*, then selecting *Items*. Select an item in the list to see the raw JSON.

    ![The raw data for one item](../images/cosmos-db-data-explorer-view-item-from-data.png)

### Visualize the data using a Jupyter notebook

As well as viewing raw data, you can also visualize data in Cosmos DB using a [Jupyter notebook](https://jupyter.org/) - a document that can contain a mixture of documentation and runnable code. Jupyter notebooks can be run inside of your Cosmos DB account, with access to all yur databases and collections, providing a convenient way to query and visualize data. You can read more on the Jupyter support in the [Built-in Jupyter Notebooks support in Azure Cosmos DB documentation](https://docs.microsoft.com/azure/cosmos-db/cosmosdb-jupyter-notebooks?WT.mc_id=academic-7372-jabenn).

1. This repo contains a Jupyter notebook to visualize the spike data. It is called [Plot_Spikes.ipynb](./notebooks/Plot_Spikes.ipynb) and is in the [notebooks](./notebooks) folder. Download this notebook.

1. From the *Data explorer*, expand the **NOTEBOOKS** node

1. Select the **...** button next to *My Notebooks*, then select **Upload File**. The button only appears when your cursor is over the *My Notebooks* section.

    ![The upload file option](../images/cosmos-db-data-explorer-upload-notebook-menu-option.png)

    > To use Jupyter notebooks in Cosmos DB you need to turn this feature on when creating the account. If you do not see the *My Notebooks* section, then you will need to recreate the Cosmos DB account.

1. Select the **Browse** button next to the file name box and locate the `Plot_Spikes.ipynb` file that you downloaded.

1. Select the **Upload** button

    ![The upload file dialog](../images/cosmos-db-data-explorer-upload-notebook-details.png)

1. The notebook will appear in the *My Notebooks* section. Select it to load it.

    ![The notebook list](../images/cosmos-db-data-explorer-notebook-list.png)

1. Wait for the Kernel to connect - this is the core 'engine' that allows the notebook to run. It is ready when the Kernel selection shows *Python 3*

    ![THe kernel loaded and ready to run Python 3 code](../images/cosmos-db-data-explorer-notebook-kernel-loaded.png)

1. From the menu, drop down the *Run* box and select the **Run All** option

    ![The run all option](../images/cosmos-db-data-explorer-notebook-run-all.png)

    Jupyter notebooks are made up of cells - boxes that can contain code or documentation. You can run these cells one at a time, or all in order. **Run All** will run them all in order, but feel free to read the documentation in the notebook and try out the cells one by one if you want to dive deeper into how it works.

1. The cells will run, pulling the last 1,000 records from Cosmos DB for the *Pi environment monitor*. It will dump out the raw data so you can validate it is working, then plot 2 graphs. The first graph will be the sound level vs time, the second will be spikes vs time.

    From these graphs you will be able to visualize the sound spikes, and these should correlate with higher sound levels.

    ![The graphs showing a correlation between sound spikes and high sound levels](../images/cosmos-db-data-explorer-notebook-graphs.png)

## Next steps

In this step you performed more advanced analytics to detect and visualize anomalies in the data.

In the [next step](./add-more-sensors.md) you will see how to add more sensors to the project to capture more data.
