"use client";


import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import LoginButton from './Login';
import MenuButton from './MenuButton';
import ThreadsPropsType from '../types/ThreadProps';
import PersistentDrawerLeft from './PersistentDrawerLeft';
import GetThreadList from "@/app/api/GetThreadList";
import SessionPropsType from "../types/SessionProps"


const Header = (props: SessionPropsType) => {
  const [open, setOpen] = React.useState(false);
  const [ThreadList, setThreadList] = React.useState<ThreadsPropsType[]>([]);
  React.useEffect(() => {
    const AxiosFunction = async () => {
      if (props.SessionUser) {
        const threadlist = await GetThreadList(props.SessionUser?.id);
        setThreadList(threadlist);
      }
    };
    AxiosFunction();
  }, [props.SessionUser]);
  console.log(ThreadList);
  return (
    <div style={{ width: "100%" }}>
      <AppBar position="static">
        <Toolbar>
          <MenuButton open={open} setOpen={setOpen} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Kada GPT
          </Typography>
          <LoginButton SessionUser={props.SessionUser} />
        </Toolbar>
      </AppBar>
      {props.SessionUser && (
        <PersistentDrawerLeft
          open={open}
          setOpen={setOpen}
          threadlist={ThreadList}
          userid={props.SessionUser?.id}
        />
      )}
    </div>
  );
};

export default Header
