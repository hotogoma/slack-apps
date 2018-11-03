const aws = require('aws-sdk');
const dynamodb = new aws.DynamoDB({region: 'us-east-1'});
const tablename = process.env.TABLE_NAME;
const maxCountNum = process.env.MAX_COUNT_NUM; 

function ParameterException(message) {
    this.message = message;
    this.name = 'ParamaterException';
}

exports.handler = async (event) => {
    try {
        // データの登録
        // クエリパラメータの取得
        const nomikaiDate = event.queryStringParameters.text;
        // yyyy/mm/dd の形式かチェック
        if (nomikaiDate.match(/^[0-9]{4}\/[0-9]{2}\/[0-9]{2}$/) === null) {
            throw new ParameterException('paramater is not date patern of yyyy/mm/dd');
        }

        // データの登録
        const putItem = await dynamodb.putItem({
            TableName: tablename,
            Item: {
                'id': {"S": nomikaiDate}
            }
        }).promise();
        
        // 登録されたデータ数をカウントする
        const scanData = await dynamodb.scan({TableName: tablename}, function(err, data) {
            if (err) console.log(err, err.stack); // an error occurred
            else     return data;  
        }).promise();
 
        const itemTotalNum = scanData.Count;

        // レスポンス用のデータ整形
        const responceBodyText = '残り' + (maxCountNum - itemTotalNum) + '回';
        const body = {
            'response_type': 'in_channel',
            'attachments': [
                {
                    text: responceBodyText,
                }
            ],
        };
        
        return  {
            'statusCode': 200,
            'headers': {},
            'body': JSON.stringify(body),
        };
    } catch (err) {
        console.error(`[Error]: ${JSON.stringify(err)}`);
        return err;
    }
};