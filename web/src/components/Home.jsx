import React, { useEffect, useState } from 'react';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Divider from '@material-ui/core/Divider';
import { makeStyles } from '@material-ui/core/styles';


import { getBasicInfos } from "../requests";

const useStyles = makeStyles((theme) => ({
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,

  },
  pos: {
    marginBottom: 12,
    marginTop: 12,
    fontSize: 12
  },
  temp: {
    fontSize: 24,

  },

}));


const Home = () => {
  const [labelsData, setLabelsData] = useState([]);
  const classes = useStyles();

  useEffect(() => {
    getBasicInfos().then(res => {
      setLabelsData(res.data);
    })
      .catch(e => {
        console.log(e);
      });
  }, []);


  return (
    <Grid container spacing={3}>
      {labelsData.map(label =>
      (
        <Grid item xs={12} sm={6} md={4} lg={3}>
          <Card>
            <CardContent>
              <Typography className={classes.title} color="textSecondary" gutterBottom>
                {label.label_id}
              </Typography>
              <Typography className={classes.temp} variant="h2" component="h2">
                {label.temp} °C
              </Typography>
              <Typography className={classes.pos} color="textSecondary">
                Letzte Messung<br></br>
                {label.datetime}
              </Typography>
            </CardContent>
            <CardActions>
              <Button size="small">Details</Button>
            </CardActions>
          </Card>
        </Grid>
      )

      )}
    </Grid>
  )
}


export default Home;