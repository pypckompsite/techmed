"use client"

import * as React from "react"
import {NavMain} from "@/components/sidebar-components/nav-main"
import {NavProjects} from "@/components/sidebar-components/nav-projects"
import {NavUser} from "@/components/sidebar-components/nav-user"
import {TeamSwitcher} from "@/components/sidebar-components/team-switcher"
import {
    Sidebar,
    SidebarContent,
    SidebarFooter,
    SidebarHeader,
    SidebarRail,
} from "@/components/ui/sidebar"
import data from "@/components/sidebar-components/user-sidebar-data";

export function AppSidebar({...props}) {
    return (
        (<Sidebar collapsible="icon" {...props}>
            <SidebarHeader>
                <TeamSwitcher teams={data.teams}/>
            </SidebarHeader>
            <SidebarContent>
                <NavMain items={data.navMain}/>
                <NavProjects projects={data.projects}/>
            </SidebarContent>
            <SidebarFooter>
                <NavUser user={data.user}/>
            </SidebarFooter>
            <SidebarRail/>
        </Sidebar>)
    );
}
